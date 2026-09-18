from django.conf import settings
from django.db import models


class Course(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1 - Principiante'),
        ('A2', 'A2 - Básico'),
        ('B1', 'B1 - Intermedio'),
        ('B2', 'B2 - Intermedio Alto'),
        ('C1', 'C1 - Avanzado'),
        ('C2', 'C2 - Maestría'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_student': True},
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student} → {self.course} ({self.progress}%)"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()
    estimated_minutes = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def is_unlocked_for(self, student):
        return Progress.objects.filter(
            student=student,
            lesson=self,
            status__in=["in_progress", "completed"]
        ).exists()

class Progress(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("in_progress", "En progreso"),
        ("completed", "Completado"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="progress"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    completion_percent = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "lesson")

    def is_accessible(self):
        return self.status in ("in_progress", "completed")


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('html', 'App HTML interactiva'),
        ('json', 'Ejercicios JSON'),
        ('py', 'Script Python'),
        ('other', 'Otro'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    file_path = models.CharField(max_length=500)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='html')
    category = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return self.title



class InteractiveQuestion(models.Model):
    """Pregunta interactiva generada desde un recurso JSON."""

    TIPOS = [
        ('mcq', 'Seleccion multiple'),
        ('true_false', 'Verdadero / Falso'),
        ('fill_blank', 'Completar'),
        ('short', 'Respuesta corta'),
        ('open', 'Respuesta abierta'),
    ]

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='interactive_questions'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interactive_questions'
    )
    text = models.TextField(verbose_name='Pregunta')
    question_type = models.CharField(max_length=20, choices=TIPOS, default='short')
    correct_answer = models.TextField(blank=True, verbose_name='Respuesta correcta')
    explanation = models.TextField(blank=True, verbose_name='Explicacion')
    options = models.JSONField(default=list, blank=True, verbose_name='Opciones')
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Pregunta interactiva'
        verbose_name_plural = 'Preguntas interactivas'

    def __str__(self):
        return self.text[:60]
