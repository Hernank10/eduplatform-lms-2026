from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Resource, InteractiveQuestion
from accounts.models import User
from gamification.models import Achievement


def home(request):
    """Pagina principal publica con estadisticas."""
    return render(request, 'home.html', {
        'total_cursos': Course.objects.filter(is_published=True).count(),
        'total_recursos': Resource.objects.filter(is_valid=True).count(),
        'total_preguntas': InteractiveQuestion.objects.count(),
        'total_usuarios': User.objects.count(),
        'total_logros': Achievement.objects.count(),
        'cursos_destacados': Course.objects.filter(is_published=True).order_by('-created_at')[:6],
        'recursos_populares': Resource.objects.filter(is_valid=True, resource_type='html')[:6],
        'logros': Achievement.objects.all()[:8],
    })


@login_required
def dashboard_redirect(request):
    """Redirige al dashboard segun el rol."""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/courses/teacher/dashboard/')
    return redirect('/courses/student/dashboard/')
