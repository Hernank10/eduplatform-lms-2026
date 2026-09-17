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
# Submission (Entregas Combinadas)
# ─────────────────────────────
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    # Usamos los campos nuevos: grade e is_graded
    list_display = ('student', 'assessment', 'submitted_at', 'grade', 'is_graded')
    list_filter = ('is_graded', 'submitted_at')
    
    # Organizamos los campos para que sea cómodo corregir
    fieldsets = (
        ('Información del Estudiante', {
            'fields': ('student', 'assessment', 'submitted_at')
        }),
        ('Trabajo Entregado', {
            'fields': ('handwritten_work', 'transcription')
        }),
        ('Evaluación del Profesor', {
            'fields': ('grade', 'teacher_feedback', 'is_graded')
        }),
    )
    readonly_fields = ('submitted_at',)
