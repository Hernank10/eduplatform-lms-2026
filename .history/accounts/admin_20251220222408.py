from django.contrib import admin
from .models import Course, Enrollment, Lesson, Progress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "level", "is_published", "created_at")
    list_filter = ("level", "is_published")
    search_fields = ("title", "description")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    list_filter = ("course",)
    search_fields = ("student__username", "course__title")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    ordering = ("course", "order")


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "status", "completion_percent", "updated_at")
    list_filter = ("status",)
    search_fields = ("student__username", "lesson__title")
