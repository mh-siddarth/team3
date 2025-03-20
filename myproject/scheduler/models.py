# models.py
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ScheduledTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
    )

    name = models.CharField(max_length=200)
    scheduled_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    task_id = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    activation_method = models.CharField(max_length=50, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_activation_methods_for_model(instance):
        if instance is None:
            return []
        
        # Filter only callable methods and exclude managers or attributes
        methods = [
            func for func in dir(instance)
            if callable(getattr(instance, func, None))  # Ensure it is callable
            and not func.startswith('_')  # Exclude dunder methods
            and not isinstance(getattr(instance.__class__, func, None), property)  # Exclude properties
            and not isinstance(getattr(instance.__class__, func, None), models.Manager)  # Exclude model managers
        ]
        
        return [(method, method.replace('_', ' ').title()) for method in methods]

    def get_activation_methods(self):
        if self.content_object:
            return self.get_activation_methods_for_model(self.content_object)
        return [('set_active', 'Set Active')]  # Default fallback option

    def __str__(self):
        return f"{self.name} - {self.status}"