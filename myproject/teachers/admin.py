from django.contrib import admin
from django.utils import timezone
from .models import Teacher
from scheduler.models import ScheduledTask
from django.contrib.contenttypes.models import ContentType

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'status', 'scheduled_task_id')
    list_filter = ('subject',)
    search_fields = ('name', 'email', 'subject')
    actions = ['schedule_status_change_now', 'schedule_status_change_in_5_minutes']

    def scheduled_task_id(self, obj):
        """Fetch the scheduled task ID for the teacher."""
        task = ScheduledTask.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        ).first()
        return task.task_id if task and task.task_id else 'Not Scheduled'
    
    scheduled_task_id.short_description = 'Scheduled Task ID'

    def schedule_status_change_now(self, request, queryset):
        """Schedule a status change in 10 seconds."""
        for teacher in queryset:
            activation_time = timezone.now() + timezone.timedelta(seconds=10)
            teacher.schedule_status_change(activation_time)
            self.message_user(request, f"Scheduled status change for {teacher.name} at {activation_time}")
    
    schedule_status_change_now.short_description = "Schedule status change now (in 10 seconds)"

    def schedule_status_change_in_5_minutes(self, request, queryset):
        """Schedule a status change in 5 minutes."""
        for teacher in queryset:
            activation_time = timezone.now() + timezone.timedelta(minutes=5)
            teacher.schedule_status_change(activation_time)
            self.message_user(request, f"Scheduled status change for {teacher.name} at {activation_time}")
    
    schedule_status_change_in_5_minutes.short_description = "Schedule status change in 5 minutes"

admin.site.register(Teacher, TeacherAdmin)
