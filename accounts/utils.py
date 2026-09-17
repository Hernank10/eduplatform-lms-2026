from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import translation
import pytz

def enviar_leccion_si_esta_despierto(estudiante, leccion_nombre):
    # 1. Obtener la zona horaria del perfil del alumno
    zona_horaria_str = estudiante.profile.timezone
    zona_alumno = pytz.timezone(zona_horaria_str)
    
    # 2. Calcular la hora actual en el país del estudiante
    hora_local_alumno = timezone.now().astimezone(zona_alumno)
    
    # 3. Definir "Hora de Despertar" (ejemplo: entre 8 AM y 9 PM)
    if 8 <= hora_local_alumno.hour < 21:
        # ACTIVAR IDIOMA Y ENVIAR
        with translation.override(estudiante.profile.language):
            asunto = translation.gettext("Nueva lección: %s") % leccion_nombre
            contenido_html = render_to_string('emails/bienvenida.html', {
                'user': estudiante,
                'leccion': leccion_nombre
            })
            
            email = EmailMessage(
                subject=asunto,
                body=contenido_html,
                from_email='escuela@redaccionglobal.com',
                to=[estudiante.email],
            )
            email.content_subtype = "html"
            email.send()
            print(f"Correo enviado a {estudiante.username} en su hora local: {hora_local_alumno.strftime('%H:%M')}")
    else:
        # Aquí podrías programarlo para más tarde o simplemente registrar que no se envió
        print(f"El estudiante {estudiante.username} está durmiendo ({hora_local_alumno.hour}h). No enviado.")
