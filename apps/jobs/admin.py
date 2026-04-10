from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'platform', 'user', 'created_at')
    search_fields = ('title', 'company', 'location', 'platform')
    list_filter = ('platform', 'created_at')
    


