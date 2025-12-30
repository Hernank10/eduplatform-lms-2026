from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "teacher", "is_published", "created_at")
    list_filter = ("level", "is_published")
    search_fields = ("title", "description")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at", "progress")
    list_filter = ("course",)
    search_fields = ("student__username", "course__title")
