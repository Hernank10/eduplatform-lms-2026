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
    description = models.TextField(blank=True)

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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    score = models.FloatField(default=0)
    passed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.assessment} ({self.score}%)"

