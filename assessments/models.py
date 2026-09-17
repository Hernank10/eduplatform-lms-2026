from django.db import models
from django.conf import settings
from courses.models import Course, Lesson

User = settings.AUTH_USER_MODEL


class Assessment(models.Model):
    ASSESSMENT_TYPES = [
        ("quiz", "Quiz"),
        ("exam", "Examen"),
        ("practice", "Práctica"),
        ("diagnostic", "Diagnóstico"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField( blank=True, null=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assessments"
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assessments"
    )

    assessment_type = models.CharField(
        max_length=20,
        choices=ASSESSMENT_TYPES,
        default="quiz"
    )

    passing_score = models.FloatField(default=60)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ("mcq", "Selección múltiple"),
        ("true_false", "Verdadero / Falso"),
        ("short", "Respuesta corta"),
    ]

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default="mcq"
    )

    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:60]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text


class Submission(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    assessment = models.ForeignKey(
        "assessments.Assessment",
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    
    # El corazón del sistema combinado
    handwritten_work = models.ImageField(
        upload_to='handwriting_submissions/%Y/%m/%d/',
        verbose_name="Foto del Manuscrito",
        null=True, blank=True
    )
    transcription = models.TextField(
        verbose_name="Transcripción Digital",
        blank=True
    )
    
    # Evaluación Docente
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    teacher_feedback = models.TextField(blank=True, verbose_name="Corrección del Profesor")
    is_graded = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrega de {self.student.username} - {self.assessment.title}"
