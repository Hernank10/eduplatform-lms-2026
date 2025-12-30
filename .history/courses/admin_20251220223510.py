from django.contrib import admin
from .models import Course, Enrollment, Lesson, Progress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "level", "is_published", "created_at")
    list_filter = ("level", "is_published")
    search_fields = ("title",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    list_filter = ("course",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    ordering = ("course", "order")


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "status", "completion_percent")
    list_filter = ("status",)

