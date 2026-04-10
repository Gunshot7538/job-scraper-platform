from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):

    PLATFORM_CHOICES = [
        ('linkedin' , 'LinkedIn'),
        ('indeed' , 'Indeed'),
        ('naukri' , 'Naukri'),  
    ]

    JOB_TYPE_CHOICES = [
        ('full-time' , 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('onsite', 'Onsite'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'jobs')
    title = models.CharField(max_length = 150)
    company = models.CharField(max_length=100 , blank=True , null=True)
    location = models.CharField(max_length=100 , blank=True , null=True)

    salary = models.CharField(max_length=100 , blank=True , null=True)
    experience = models.CharField(max_length=50 , blank=True, null=True)
    skills = models.TextField(blank=True , null=True)

    job_type = models.CharField(max_length=100 ,choices= JOB_TYPE_CHOICES ,  blank=True , null=True)

    posted_date = models.CharField(max_length=50 , blank=True , null=True)

    platform = models.CharField(max_length=20 ,choices = PLATFORM_CHOICES)

    requirements = models.TextField(blank=True , null=True)
    description = models.TextField(blank=True, null=True)

    apply_link = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

     # NEW FIELDS - Add these
    match_score = models.FloatField(default=0.0, blank=True, null=True)
    star_rating = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.company} ({self.platform})"
    
    class Meta:
        ordering = ['-match_score', '-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

