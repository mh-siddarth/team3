# admin.py
from django.contrib import admin
from django import forms
from .models import ScheduledTask

@admin.register(ScheduledTask)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_id", "name", "scheduled_date", "status", "activation_method", "executed_function", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("name",)
    ordering = ("created_at",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "activation_method":
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                task = ScheduledTask.objects.filter(pk=obj_id).first()
                if task and task.content_object:
                    choices = [("", "---------")] + task.get_activation_methods()
                else:
                    choices = [("", "No content object found")]
            else:
                choices = [("", "Select a content object first")]

            return forms.ChoiceField(
                choices=choices,
                widget=forms.Select(),
                required=False,
                initial=None
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def executed_function(self, obj):
        if obj.status == "pending":
            return ""
        if obj.content_object and obj.activation_method:
            return obj.activation_method
        elif obj.content_object:
            return "No method selected"
        return "No linked object"

    executed_function.short_description = "Executed Function"