import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Enrollment, Progress, Course, Resource
from assessments.models import Submission
from django.shortcuts import render

from .models import Enrollment, Progress, Course
from assessments.models import Submission


@login_required
def student_dashboard(request):
    student = request.user
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    progress_list = Progress.objects.filter(student=student).select_related('lesson', 'lesson__course')
    recent_submissions = Submission.objects.filter(student=student).select_related('assessment').order_by('-submitted_at')[:5]

    return render(request, 'courses/student_dashboard.html', {
        'enrollments': enrollments,
        'progress_list': progress_list,
        'recent_submissions': recent_submissions,
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
