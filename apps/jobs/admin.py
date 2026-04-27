from django.contrib import admin
from .models import Job, SupportQuery

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'platform', 'user', 'created_at')
    search_fields = ('title', 'company', 'location', 'platform')
    list_filter = ('platform', 'created_at')


@admin.register(SupportQuery)
class SupportQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_message', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'message')
    list_editable = ('status',)
    readonly_fields = ('user', 'message', 'created_at', 'updated_at')

    def short_message(self, obj):
        return obj.message[:80] + '...' if len(obj.message) > 80 else obj.message
    short_message.short_description = 'Message'
