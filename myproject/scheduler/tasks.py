from celery import shared_task
from django.utils import timezone
from django.apps import apps  # Import all models dynamically
from scheduler.models import ScheduledTask

from celery import shared_task
from django.utils import timezone
from scheduler.models import ScheduledTask

@shared_task
def update_task_status():
    print(f"Running Beat task 'update_task_status' at {timezone.now()}")
    tasks = ScheduledTask.objects.filter(status='pending')

    def execute(resource, function_name,*args, **kwargs):
        """Dynamically execute a method on the given resource (model instance)."""
        if hasattr(resource, function_name):  
            method = getattr(resource, function_name)  
            if callable(method):  
                return method(*args, **kwargs)  # ✅ CALL the method instead of returning it
        return f"Function '{function_name}' not found on {resource}"

    for task in tasks:
        if timezone.now() >= task.scheduled_date:
            task.status = 'active'
            task.save()
            print(f"Beat updated task '{task}' to 'active'")

            if task.content_object:
                try:
                    result = execute(task.content_object, task.activation_method)
                    if isinstance(result, str) and result.startswith("Function"):
                        print(f"Warning: {result}")
                    else:   
                        print(f"Executed '{task.activation_method}' on {task.content_object}, result: {result}")
                except Exception as e:
                    print(f"Error executing '{task.activation_method}' on {task.content_object}: {e}")
























# @shared_task(bind=True)
# def activate_task(self, task_id):
#     print(f"Executing ETA task for task_id: {task_id} at {self.request.eta}")
#     try:
#         task = ScheduledTask.objects.get(id=task_id)
#         print(f"Found task: '{task.name}', status: {task.status}, scheduled: {task.scheduled_date}")
        
#         # Only proceed if task is still pending and time has arrived
#         if task.status == 'pending' and timezone.now() >= task.scheduled_date:
#             # Check if linked to a student
#             if task.content_object and isinstance(task.content_object, Students):
#                 student = task.content_object
#                 print(f"Task linked to student: '{student.name}', status: {student.status}")
#                 if student.status == 'pending':
#                     student.set_active()  # Update student status
#                 else:
#                     print(f"Student '{student.name}' already active, no change needed")
            
#             # Update task status
#             task.status = 'active'
#             task.save()
#             print(f"Task '{task.name}' updated to 'active' at {timezone.now()}")
#         else:
#             print(f"Task '{task.name}' not updated - status: {task.status}, time: {timezone.now()}")
#     except ScheduledTask.DoesNotExist:
#         print(f"Task with ID {task_id} not found")
#     except Exception as e:
#         print(f"Error executing task {task_id}: {str(e)}")
#     return "Task processed"
