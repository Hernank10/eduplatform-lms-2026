from django.contrib import admin
from .models import Achievement, UserAchievement, UserPoints, Certificate, DailyChallenge


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'puntos', 'icono')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')


@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'nivel')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'course', 'final_score', 'issued_at')


@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'titulo', 'puntos', 'activo')
