import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, get_object_or_404

from .models import Enrollment, Progress, Course, Lesson, Lesson, Resource
from assessments.models import Submission
from gamification.models import UserPoints, UserAchievement, Certificate
from django.shortcuts import render, get_object_or_404, redirect

from .models import Enrollment, Progress, Course, Lesson, Lesson
from assessments.models import Submission
from gamification.models import UserPoints, UserAchievement, Certificate


@login_required
def student_dashboard(request):
    student = request.user
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    progress_list = Progress.objects.filter(student=student).select_related('lesson', 'lesson__course')
    recent_submissions = Submission.objects.filter(student=student).select_related('assessment', 'assessment__course').order_by('-submitted_at')[:5]

    # Cursos con progreso
    cursos_data = []
    for enrollment in enrollments:
        course = enrollment.course
        lessons = course.lessons.all()
        progress_lessons = Progress.objects.filter(student=student, lesson__course=course)

        total = lessons.count()
        completed = progress_lessons.filter(status='completed').count()
        in_progress = progress_lessons.filter(status='in_progress').count()
        percent = int((completed / total) * 100) if total > 0 else 0

        # Logros del curso
        logros_curso = UserAchievement.objects.filter(
            user=student,
            achievement__codigo='course_complete'
        ).count()

        # Certificado del curso
        cert = Certificate.objects.filter(user=student, course=course).first()

        cursos_data.append({
            'enrollment': enrollment,
            'course': course,
            'lessons_total': total,
            'lessons_completed': completed,
            'lessons_in_progress': in_progress,
            'percent': percent,
            'certificado': cert,
        })

    # Gamificacion
    puntos, _ = UserPoints.objects.get_or_create(user=student)
    mis_logros = UserAchievement.objects.filter(user=student).select_related('achievement')[:6]
    total_logros = UserAchievement.objects.filter(user=student).count()
    total_certificados = Certificate.objects.filter(user=student).count()

    return render(request, 'courses/student_dashboard.html', {
        'enrollments': enrollments,
        'progress_list': progress_list,
        'recent_submissions': recent_submissions,
        'cursos_data': cursos_data,
        'total_cursos': enrollments.count(),
        'total_lecciones_completadas': progress_list.filter(status='completed').count(),
        'puntos': puntos,
        'mis_logros': mis_logros,
        'total_logros': total_logros,
        'total_certificados': total_certificados,
    })

@login_required
def teacher_dashboard(request):
    teacher = request.user
    courses = Course.objects.filter(teacher=teacher)
    submissions = Submission.objects.filter(assessment__lesson__course__in=courses).select_related('student', 'assessment').order_by('-submitted_at')
    blocked_progress = Progress.objects.filter(lesson__course__in=courses, status__in=['pending', 'in_progress'])
    pending_grading = submissions.filter(is_graded=False)

    return render(request, 'courses/teacher_dashboard.html', {
        'courses': courses,
        'submissions': submissions,
        'blocked_progress': blocked_progress,
        'pending_grading': pending_grading,
    })


@login_required
def resource_list(request):
    tipo = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')

    recursos = Resource.objects.filter(is_valid=True)
    if tipo:
        recursos = recursos.filter(resource_type=tipo)
    if categoria:
        recursos = recursos.filter(category__icontains=categoria)

    categorias = Resource.objects.filter(is_valid=True).values_list('category', flat=True).distinct().order_by('category')
    categorias = [c for c in categorias if c]

    return render(request, 'courses/resource_list.html', {
        'recursos': recursos,
        'categorias': categorias,
        'tipo_filtro': tipo,
        'categoria_filtro': categoria,
    })


@login_required
def resource_detail(request, pk):
    recurso = get_object_or_404(Resource, pk=pk)
    contenido = None

    if recurso.resource_type == 'html':
        try:
            base_dir = r'E:\02_proyectos\eduplatform\ejercicios_completos-lengua-castellana'
            full_path = os.path.join(base_dir, recurso.file_path)
            with open(full_path, encoding='utf-8') as f:
                contenido = f.read()
        except Exception as e:
            contenido = f'Error al leer: {e}'

    return render(request, 'courses/resource_detail.html', {
        'recurso': recurso,
        'contenido': contenido,
    })


@login_required
def course_list(request):
    """Lista de cursos publicados."""
    cursos = Course.objects.filter(is_published=True).select_related('teacher')

    # Si el usuario es estudiante, mostrar sus inscripciones
    mis_inscripciones = []
    if request.user.is_student:
        mis_inscripciones = Enrollment.objects.filter(
            student=request.user
        ).values_list('course_id', flat=True)

    return render(request, 'courses/course_list.html', {
        'cursos': cursos,
        'mis_inscripciones': list(mis_inscripciones),
    })


@login_required
def course_detail(request, pk):
    """Detalle de un curso con sus lecciones."""
    curso = get_object_or_404(Course, pk=pk)
    lecciones = curso.lessons.all().order_by('order')

    # Verificar si el estudiante esta inscrito
    inscrito = False
    if request.user.is_student:
        inscrito = Enrollment.objects.filter(
            student=request.user, course=curso
        ).exists()

    # Progreso del estudiante en este curso
    progreso = {}
    if inscrito:
        for p in Progress.objects.filter(student=request.user, lesson__course=curso):
            progreso[p.lesson_id] = p

    # Evaluaciones del curso
    evaluaciones = curso.assessments.all()

    # Certificado (si lo tiene)
    certificado = None
    try:
        from gamification.models import Certificate
        certificado = Certificate.objects.filter(user=request.user, course=curso).first()
    except Exception:
        pass

    return render(request, 'courses/course_detail.html', {
        'curso': curso,
        'lecciones': lecciones,
        'inscrito': inscrito,
        'progreso': progreso,
        'evaluaciones': evaluaciones,
        'certificado': certificado,
    })


@login_required
def lesson_detail(request, pk):
    """Detalle de una leccion."""
    leccion = get_object_or_404(Lesson, pk=pk)
    curso = leccion.course

    # Verificar inscripcion
    inscrito = False
    if request.user.is_student:
        inscrito = Enrollment.objects.filter(
            student=request.user, course=curso
        ).exists()

    # Progreso de esta leccion
    progreso = None
    if inscrito:
        progreso, _ = Progress.objects.get_or_create(
            student=request.user,
            lesson=leccion,
            defaults={'status': 'in_progress', 'completion_percent': 0}
        )

    # Lecciones anterior y siguiente
    lecciones = list(curso.lessons.all().order_by('order'))
    idx = next((i for i, l in enumerate(lecciones) if l.id == leccion.id), -1)
    anterior = lecciones[idx - 1] if idx > 0 else None
    siguiente = lecciones[idx + 1] if idx < len(lecciones) - 1 else None

    # Evaluaciones de esta leccion
    evaluaciones = leccion.assessments.all()

    return render(request, 'courses/lesson_detail.html', {
        'leccion': leccion,
        'curso': curso,
        'inscrito': inscrito,
        'progreso': progreso,
        'anterior': anterior,
        'siguiente': siguiente,
        'evaluaciones': evaluaciones,
    })


@login_required
def course_enroll(request, pk):
    """Inscribirse en un curso."""
    curso = get_object_or_404(Course, pk=pk)

    if request.method == 'POST' and request.user.is_student:
        Enrollment.objects.get_or_create(student=request.user, course=curso)
        return redirect('course_detail', pk=curso.pk)

    return render(request, 'courses/course_enroll.html', {'curso': curso})


@login_required
def lesson_complete(request, pk):
    """Marcar leccion como completada."""
    leccion = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        progreso, _ = Progress.objects.get_or_create(
            student=request.user,
            lesson=leccion,
            defaults={'status': 'in_progress'}
        )
        progreso.status = 'completed'
        progreso.completion_percent = 100
        progreso.save()

        # Actualizar progreso del enrollment
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=leccion.course)
            total = leccion.course.lessons.count()
            completadas = Progress.objects.filter(
                student=request.user,
                lesson__course=leccion.course,
                status='completed'
            ).count()
            enrollment.progress = int((completadas / total) * 100) if total > 0 else 0
            enrollment.save()
        except Enrollment.DoesNotExist:
            pass

        return redirect('lesson_detail', pk=leccion.pk)

    return render(request, 'courses/lesson_complete.html', {'leccion': leccion})
