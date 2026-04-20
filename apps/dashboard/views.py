import csv
import io
from sys import platform
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.core.paginator import Paginator

from apps.jobs.models import Job
from apps.scraping.factory import scrape_jobs_by_platform
from apps.resume_parser.keyword_extractor import extract_skills


def _get_stars(score):
    if score >= 80: return 5
    elif score >= 60: return 4
    elif score >= 40: return 3
    elif score >= 20: return 2
    else: return 1


@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def dashboard_view(request):

    if request.method == 'POST':
        job_title = request.POST.get('job_title', '').strip()
        location  = request.POST.get('location', '').strip()
        platform  = request.POST.get('platform', '').strip()
        job_count = request.POST.get('job_count')

        if not job_title or not location or not platform:
            messages.error(request, "Please fill all fields.")
        else:
            try:
                job_count = int(job_count) if job_count else 20
                messages.info(request, f"Scraping {job_count} jobs for {job_title} in {location} from {platform}...")

                Job.objects.filter(user=request.user, platform=platform).delete()
                scraped_jobs = scrape_jobs_by_platform(platform, job_title, location)

                if not scraped_jobs:
                    messages.warning(request, "No jobs found or scraping failed.")
                else:
                    scraped_jobs = scraped_jobs[:100]
                    count = 0
                    for item in scraped_jobs:
                        if not Job.objects.filter(user=request.user, apply_link=item.get('apply_link')).exists():
                            Job.objects.create(
                                user=request.user,
                                title=item.get('title', '') or 'No Title',
                                company=item.get('company', ''),
                                location=item.get('location', ''),
                                salary=item.get('salary', ''),
                                experience=item.get('experience', ''),
                                skills=item.get('skills', ''),
                                job_type=item.get('job_type', ''),
                                posted_date=item.get('posted_date', ''),
                                platform=item.get('platform', platform),
                                requirements=item.get('requirements', ''),
                                description=item.get('description', ''),
                                apply_link=item.get('apply_link', 'https://www.naukri.com/'),
                            )
                            count += 1
                    messages.success(request, f"{count} jobs scraped successfully!")

            except Exception as e:
                messages.error(request, f"Scraping error: {e}")

    # ================= SEARCH =================
    search_query = request.GET.get('q', '')

    platform_filter = request.GET.get('platform', '')

    jobs = Job.objects.filter(user=request.user)

    if platform_filter:
        jobs = jobs.filter(platform=platform_filter)
    


    if search_query:
        jobs = jobs.filter(title__icontains=search_query) \
             | jobs.filter(company__icontains=search_query) \
             | jobs.filter(location__icontains=search_query)

    jobs = jobs.order_by('-created_at')

    # ================= SKILL MATCH SCORE =================
    resume_data   = request.session.get('resume_data', None)
    resume_skills = set()

    if resume_data and resume_data.get('skills'):
        resume_skills = set(s.lower().strip() for s in resume_data['skills'] if s.strip())

    jobs_with_score = []
    for job in jobs:
        job_dict = {
            'id'            : job.id,
            'title'         : job.title,
            'company'       : job.company,
            'location'      : job.location,
            'salary'        : job.salary,
            'experience'    : job.experience,
            'skills'        : job.skills,
            'job_type'      : job.job_type,
            'posted_date'   : job.posted_date,
            'platform'      : job.platform,
            'description'   : job.description,
            'requirements'  : job.requirements,
            'apply_link'    : job.apply_link,
            'match_score'   : 0,
            'match_count'   : '',
            'matched_skills': [],
            'missing_skills': [],
            'star_rating'   : 0,
        }

        if resume_skills:
            # Job ki skills nikalo
            job_skills_str = job.skills or ''
            has_explicit   = len(job_skills_str.strip()) > 5

            if has_explicit:
                # Naukri: comma separated skills directly available
                job_skills = set(s.strip().lower() for s in job_skills_str.split(',') if s.strip())
            else:
                # LinkedIn/Indeed: NLP se description se extract karo
                full_text  = ((job.description or '') + ' ' + (job.requirements or '')).strip()
                extracted  = extract_skills(full_text) if full_text else []
                job_skills = set(s.lower().strip() for s in extracted if s.strip())

            if job_skills:
                matched = resume_skills & job_skills
                missing = job_skills - resume_skills
                score   = round((len(matched) / len(job_skills)) * 100, 1)

                job_dict['match_score']    = score
                job_dict['match_count']    = f"{len(matched)}/{len(job_skills)}"
                job_dict['matched_skills'] = sorted(list(matched))
                job_dict['missing_skills'] = sorted(list(missing))
                job_dict['star_rating']    = _get_stars(score)

        jobs_with_score.append(job_dict)

    # Score ke hisaab se sort karo (sirf jab resume upload ho)
    if resume_skills:
        jobs_with_score.sort(key=lambda x: x['match_score'], reverse=True)

    # ================= STATS =================
    total_jobs_count = len(jobs_with_score)
    avg_match = 0
    if total_jobs_count > 0:
        avg_match = round(sum(j['match_score'] for j in jobs_with_score) / total_jobs_count, 1)
    
    platforms = {}
    for j in jobs_with_score:
        p = j['platform'].capitalize()
        platforms[p] = platforms.get(p, 0) + 1

    # ================= PAGINATION =================
    paginator   = Paginator(jobs_with_score, 20)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    context = {
        'jobs'           : page_obj,
        'resume_data'    : resume_data,
        'total_jobs'     : total_jobs_count,
        'avg_match'      : avg_match,
        'platform_stats' : platforms,
        'active_platform': platform_filter or (jobs_with_score[0]['platform'] if jobs_with_score else 'Global'),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/job_list_partial.html', context)

    return render(request, 'dashboard.html', context)


# ================= CSV DOWNLOAD =================
@login_required
def download_csv(request):
    jobs = Job.objects.filter(user=request.user).order_by('-created_at')
    if not jobs.exists():
        messages.warning(request, "No jobs to download.")
        return redirect('dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jobs.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title','Company','Location','Salary','Experience','Skills','Job Type','Posted Date','Platform','Requirements','Description','Apply Link'])
    for job in jobs:
        writer.writerow([job.title,job.company,job.location,job.salary,job.experience,job.skills,job.job_type,job.posted_date,job.platform,job.requirements,job.description,job.apply_link])
    return response


# ================= EMAIL SEND =================
@login_required
def send_email(request):
    if request.method == 'POST':
        jobs = Job.objects.filter(user=request.user).order_by('-created_at')
        if not jobs.exists():
            messages.warning(request, "No jobs to send.")
            return redirect('dashboard')

        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(['Title','Company','Location','Salary','Experience','Skills','Job Type','Posted Date','Platform','Apply Link'])
        for job in jobs:
            writer.writerow([job.title,job.company,job.location,job.salary,job.experience,job.skills,job.job_type,job.posted_date,job.platform,job.apply_link])

        try:
            email = EmailMessage(
                subject='Your Scraped Jobs - Smart Job Manager',
                body=f'Hi {request.user.username},\n\nYour jobs are attached.\n\nGood luck!',
                to=[request.user.email],
            )
            email.attach('jobs.csv', csv_buffer.getvalue(), 'text/csv')
            email.send()
            messages.success(request, f"Jobs sent to {request.user.email}")
        except Exception as e:
            messages.error(request, f"Email error: {e}")

    return redirect('dashboard')

