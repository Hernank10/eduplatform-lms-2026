from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Profile


def registro(request):
    """Registro de nuevos usuarios."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errores = []
        if not username:
            errores.append('El nombre de usuario es obligatorio')
        if User.objects.filter(username=username).exists():
            errores.append('Ese nombre de usuario ya existe')
        if not email:
            errores.append('El email es obligatorio')
        if User.objects.filter(email=email).exists():
            errores.append('Ese email ya esta registrado')
        if len(password1) < 6:
            errores.append('La contrasena debe tener al menos 6 caracteres')
        if password1 != password2:
            errores.append('Las contrasenas no coinciden')

        if errores:
            for e in errores:
                messages.error(request, e)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                is_student=True,
            )
            login(request, user)
            messages.success(request, 'Bienvenido, ' + username + '!')
            return redirect('dashboard')

    return render(request, 'registration/registro.html')


@login_required
def perfil(request):
    """Perfil del usuario."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        profile.language = request.POST.get('language', 'es')
        profile.save()

        messages.success(request, 'Perfil actualizado')
        return redirect('perfil')

    from courses.models import Enrollment
    from gamification.models import UserPoints, UserAchievement, Certificate

    enrollments = Enrollment.objects.filter(student=user).select_related('course')
    puntos, _ = UserPoints.objects.get_or_create(user=user)
    logros = UserAchievement.objects.filter(user=user).select_related('achievement')
    certificados = Certificate.objects.filter(user=user).select_related('course')

    return render(request, 'perfil.html', {
        'profile': profile,
        'enrollments': enrollments,
        'puntos': puntos,
        'logros': logros,
        'certificados': certificados,
    })
