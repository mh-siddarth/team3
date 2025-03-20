from django.db import models
from django.utils import timezone

class Teacher(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
    )

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.name} - {self.status}"

    def schedule_status_update(self, activation_time):
        """Create a ScheduledTask to change the teacher's status at the given time."""
        from scheduler.models import ScheduledTask
        from django.contrib.contenttypes.models import ContentType
        try:
            existing_task = ScheduledTask.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.id,
                task_id__isnull=False
            ).first()

            if not existing_task:
                if not timezone.is_aware(activation_time):
                    activation_time = timezone.make_aware(activation_time, timezone.get_default_timezone())

                task = ScheduledTask.objects.create(
                    name=f"Activate {self.name}",
                    scheduled_date=activation_time,
                    content_type=ContentType.objects.get_for_model(self),
                    object_id=self.id
                )
                task.schedule_task()
                print(f"Scheduled status change for teacher '{self.name}' at {activation_time} (Asia/Kolkata)")
            else:
                print(f"Teacher '{self.name}' already has a scheduled task with ID: {existing_task.task_id}")
        except Exception as e:
            print(f"Error scheduling status change for teacher '{self.name}': {str(e)}")

    def mark_active(self):
        """Activate teacher."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            print(f"Teacher '{self.name}' status changed to 'active' at {timezone.now()}")
        else:
            print(f"Teacher '{self.name}' status not changed - already '{self.status}'")

    def activate_with_announcement(self):
        """Activate teacher and make an announcement."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            print(f"Teacher '{self.name}' activated and announcement made at {timezone.now()}")

    def activate_with_record(self):
        """Activate teacher and record the activation event."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            print(f"Teacher '{self.name}' activated and recorded at {timezone.now()}")

    def activate_with_email_notification(self):
        """Activate teacher and send an email notification."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            print(f"Teacher '{self.name}' activated and email notification sent at {timezone.now()}")
