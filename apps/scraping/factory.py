from .naukri import scrape_naukri_jobs
from .indeed import scrape_indeed_jobs
from .linkedin import scrape_linkedin_jobs


def scrape_jobs_by_platform(platform, job_title, location):
    if platform == 'naukri':
        return scrape_naukri_jobs(job_title, location)
    elif platform == 'linkedin':
        return scrape_linkedin_jobs(job_title, location)
    elif platform == 'indeed':
        return scrape_indeed_jobs(job_title, location)
    return []