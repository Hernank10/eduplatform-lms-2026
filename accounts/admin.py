from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (
            "Roles",
            {
                "fields": (
                    "is_student",
                    "is_teacher",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "is_student",
        "is_teacher",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_student",
        "is_teacher",
        "is_staff",
        "is_active",
    )
