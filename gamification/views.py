from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Achievement, UserAchievement, UserPoints, Certificate, DailyChallenge


@login_required
def leaderboard(request):
    top = UserPoints.objects.select_related('user').order_by('-total')[:20]
    mi_puntos, _ = UserPoints.objects.get_or_create(user=request.user)
    mi_posicion = UserPoints.objects.filter(total__gt=mi_puntos.total).count() + 1

    return render(request, 'gamification/leaderboard.html', {
        'top': top,
        'mi_puntos': mi_puntos,
        'mi_posicion': mi_posicion,
    })


@login_required
def achievements(request):
    mis_logros = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    mis_ids = [ua.achievement_id for ua in mis_logros]
    disponibles = Achievement.objects.exclude(id__in=mis_ids)

    return render(request, 'gamification/achievements.html', {
        'mis_logros': mis_logros,
        'disponibles': disponibles,
    })


@login_required
def certificates(request):
    mis_certs = Certificate.objects.filter(user=request.user).select_related('course')

    return render(request, 'gamification/certificates.html', {
        'mis_certs': mis_certs,
    })


@login_required
def certificate_detail(request, code):
    cert = get_object_or_404(Certificate, code=code)

    if cert.user != request.user and not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('No tienes acceso a este certificado')

    return render(request, 'gamification/certificate_detail.html', {
        'cert': cert,
    })


@login_required
def challenge_today(request):
    from django.utils import timezone
    hoy = timezone.now().date()
    desafio = DailyChallenge.objects.filter(fecha=hoy, activo=True).first()

    return render(request, 'gamification/challenge.html', {
        'desafio': desafio,
    })
