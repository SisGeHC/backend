from django.contrib import admin
from courses.models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "coordinator", "teacher")  
    search_fields = ("name", "coordinator__email", "teacher__email")  
    list_filter = ("coordinator", "teacher")  

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            raise PermissionError("Apenas administradores podem criar cursos.")
        super().save_model(request, obj, form, change)
