from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_student", "is_teacher", "is_staff")
    list_filter = ("is_student", "is_teacher", "is_staff")
    search_fields = ("username", "email")

