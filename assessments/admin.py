from django.contrib import admin
from .models import Assessment, Question, Choice, Submission


# ─────────────────────────────
# Inline para opciones
# ─────────────────────────────
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


# ─────────────────────────────
# Inline para preguntas
# ─────────────────────────────
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


# ─────────────────────────────
# Assessment
# ─────────────────────────────
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)
    search_fields = ("title",)
    inlines = [QuestionInline]


# ─────────────────────────────
# Question
# ─────────────────────────────
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "assessment", "points")
    inlines = [ChoiceInline]


# ─────────────────────────────
# Submission
# ─────────────────────────────
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "assessment", "score", "submitted_at")
    readonly_fields = ("submitted_at",)

