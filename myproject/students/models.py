
from django.db import models
from django.utils import timezone

class Students(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
    )

    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.name} - {self.status}"

    def schedule_status_change(self, activation_time):
        """Create a ScheduledTask to change the student's status at the given time."""
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
                print(f"Scheduled status change for student '{self.name}' at {activation_time} (Asia/Kolkata)")
            else:
                print(f"Student '{self.name}' already has a scheduled task with ID: {existing_task.task_id}")
        except Exception as e:
            print(f"Error scheduling status change for student '{self.name}': {str(e)}")

    def set_active(self):
        """Activate student."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            print(f"Student '{self.name}' status changed to 'active' at {timezone.now()}")
        else:
            print(f"Student '{self.name}' status not changed - already '{self.status}'")

    def activate_with_notification(self):
        """Activate student and send a notification."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            print(f"Student '{self.name}' activated and notified at {timezone.now()}")

    def activate_with_log(self):
        """Activate student and log the activation event."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            # Log activation (this can be replaced with an actual logging mechanism)
            print(f"Student '{self.name}' activated and logged at {timezone.now()}")

    def activate_with_welcome_email(self):
        """Activate student and send a welcome email."""
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            # Placeholder for sending an email (can integrate Django's Email framework)
            print(f"Student '{self.name}' activated and welcome email sent at {timezone.now()}")

    # def srinathhh(self):
    #     """Srinath's special method."""
    #     return "selected for dubai"c