from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Achievement(models.Model):
    TIPOS = [
        ('first_lesson', 'Primera leccion completada'),
        ('ten_lessons', '10 lecciones completadas'),
        ('fifty_lessons', '50 lecciones completadas'),
        ('course_complete', 'Curso completado'),
        ('first_certificate', 'Primer certificado'),
        ('perfect_score', 'Puntuacion perfecta'),
        ('five_courses', 'Inscrito en 5 cursos'),
        ('streak_7', 'Racha de 7 dias'),
    ]

    codigo = models.CharField(max_length=50, choices=TIPOS, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, default='TROFEO')
    puntos = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['puntos', 'nombre']

    def __str__(self):
        return self.nombre


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='users')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-earned_at']

    def __str__(self):
        return self.user.username + ' - ' + self.achievement.nombre


class UserPoints(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='points')
    total = models.PositiveIntegerField(default=0)
    nivel = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Puntos de usuario'
        verbose_name_plural = 'Puntos de usuarios'

    def calcular_nivel(self):
        return (self.total // 100) + 1

    def add_points(self, cantidad):
        self.total += cantidad
        self.nivel = self.calcular_nivel()
        self.save()

    def __str__(self):
        return self.user.username + ': ' + str(self.total) + ' pts'

class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    final_score = models.FloatField(default=0)

    # Campos para el diploma
    teacher_name = models.CharField(max_length=200, blank=True)
    teacher_title = models.CharField(max_length=200, blank=True, default='Profesor del curso')
    director_name = models.CharField(max_length=200, blank=True)
    director_title = models.CharField(max_length=200, blank=True, default='Director Academico')
    institution = models.CharField(max_length=200, blank=True, default='EduPlatform - Espanol Global')

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-issued_at']

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:12].upper()
        # Auto-rellenar nombres
        if not self.teacher_name and self.course and self.course.teacher:
            self.teacher_name = self.course.teacher.get_full_name() or self.course.teacher.username
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Certificado ' + self.code + ' - ' + self.user.username

class DailyChallenge(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    puntos = models.PositiveIntegerField(default=20)
    fecha = models.DateField(default=timezone.now)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        unique_together = ('fecha', 'titulo')

    def __str__(self):
        return self.fecha.isoformat() + ' - ' + self.titulo
