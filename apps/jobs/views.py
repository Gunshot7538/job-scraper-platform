from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Job
from apps.resume_parser.pdf_extractor import extract_text_from_file
from apps.resume_parser.keyword_extractor import (
    extract_skills, extract_experience, extract_location, extract_email
)
from apps.resume_parser.matcher import calculate_job_match, get_star_rating
import json

from django.core.paginator import Paginator


def job_list(request):
    """Show all jobs, with resume matching if resume uploaded"""
    jobs = Job.objects.all().order_by('-match_score', '-id')
    
    resume_data = request.session.get('resume_data', None)

     # Pagination — 20 jobs per page = 3 pages = 60 jobs
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,          # ← jobs ki jagah page_obj
        'resume_data': resume_data,
        'total_jobs': jobs.count(),
        'page_obj': page_obj,
    }
    return render(request, 'jobs/job_list.html', context)


def upload_resume(request):
    """Handle resume upload and match with jobs"""
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        
        if not resume_file:
            messages.error(request, 'Please upload a resume file.')
            return redirect('dashboard')
        
        # Check file type
        allowed_types = ['.pdf', '.docx', '.doc']
        file_name = resume_file.name.lower()
        if not any(file_name.endswith(ext) for ext in allowed_types):
            messages.error(request, 'Only PDF and DOCX files are allowed.')
            return redirect('dashboard')
        
        try:
            # Extract text from resume
            resume_text = extract_text_from_file(resume_file)
            
            if not resume_text:
                messages.error(request, 'Could not extract text from resume.')
                return redirect('dashboard')
            
            # Extract info from resume
            resume_data = {
                'text': resume_text,
                'skills': extract_skills(resume_text),
                'experience': extract_experience(resume_text),
                'location': extract_location(resume_text),
                'email': extract_email(resume_text),
            }
            
            # Save resume data in session
            request.session['resume_data'] = {
                'skills': resume_data['skills'],
                'experience': resume_data['experience'],
                'location': resume_data['location'],
                'email': resume_data['email'],
            }
            
            # Match each job with resume and update DB
            jobs = Job.objects.all()
            for job in jobs:
                job_dict = {
                    'skills': job.skills,
                    'description': job.description,
                    'requirements': job.requirements,
                    'experience': job.experience,
                    'location': job.location,
                }
                result = calculate_job_match(resume_data, job_dict)
                score = result[0] if isinstance(result, tuple) else result
                job.match_score = float(score)
                job.star_rating = get_star_rating(score)
                job.save()
            
            matched_count = Job.objects.filter(match_score__gte=40).count()
            messages.success(
                request, 
                f'Resume analyzed! Found {matched_count} matching jobs. '
                f'Skills detected: {", ".join(resume_data["skills"][:5])}'
            )
            
        except Exception as e:
            messages.error(request, f'Error processing resume: {str(e)}')
        
        return redirect('dashboard')
    
    return redirect('dashboard')

def clear_resume(request):
    if 'resume_data' in request.session:
        del request.session['resume_data']
    Job.objects.filter(user=request.user).update(match_score=0.0, star_rating=0)
    messages.info(request, 'Resume cleared. Showing all jobs.')
    return redirect('dashboard')  # ← dashboard pe wapas