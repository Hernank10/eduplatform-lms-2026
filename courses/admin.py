from django.contrib import admin
from .models import Course, Enrollment, Lesson, Progress, Resource


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
    list_display = (
        "student",
        "lesson",
        "status",
        "completion_percent",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = (
        "student__username",
        "lesson__title",
        "lesson__course__title",
    )
    readonly_fields = ("updated_at",)
 

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'category', 'file_size', 'is_valid', 'created_at')
    list_filter = ('resource_type', 'category', 'is_valid')
    search_fields = ('title', 'description', 'category')
    readonly_fields = ('created_at',)
