
"""
cargar_recursos.py
Escanea la carpeta de ejercicios y crea registros Resource en la BD.
"""
import os
import sys

# IMPORTANTE: los sys.path.insert van ANTES de importar django
sys.path.insert(0, r'E:\PythonPortable_Django5\Lib\site-packages')
sys.path.insert(0, r'E:\02_proyectos\eduplatform\_original')

import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduplatform.settings')
django.setup()

from courses.models import Resource


BASE_DIR = r'E:\02_proyectos\eduplatform\_original'
EJERCICIOS_DIR = r'E:\02_proyectos\eduplatform\ejercicios_completos-lengua-castellana'


def es_json_valido(path):
    try:
        with open(path, encoding='utf-8') as f:
            json.load(f)
        return True
    except Exception:
        return False


def extraer_categoria(nombre):
    palabras_clave = [
        'Retorica', 'Narrativa', 'Fonetica', 'Morfologia', 'Sintaxis',
        'Semantica', 'Ortografia', 'Redaccion', 'Caligrafia', 'Lexicografia',
        'Etimologia', 'Literatura', 'Gramatica', 'Pragmatica', 'Sociolinguistica',
        'Psicolinguistica', 'Antropolinguistica', 'Textolinguistica', 'Etnolinguistica',
        'Puntuacion', 'Conectores', 'Parrafo', 'Oracion', 'Verbo', 'Adjetivo',
        'Sustantivo', 'Preposicion', 'Adverbio', 'Pronombre',
    ]
    for p in palabras_clave:
        if p.lower() in nombre.lower():
            return p
    return 'General'


def main():
    print('=== CARGANDO RECURSOS ===')
    print('Carpeta:', EJERCICIOS_DIR)
    print()

    if not os.path.exists(EJERCICIOS_DIR):
        print('ERROR: no existe la carpeta')
        return

    Resource.objects.all().delete()
    print('Recursos anteriores eliminados')

    archivos = [f for f in os.listdir(EJERCICIOS_DIR) if os.path.isfile(os.path.join(EJERCICIOS_DIR, f))]
    print('Archivos encontrados:', len(archivos))
    print()

    creados = 0
    saltados = 0

    for nombre in archivos:
        full_path = os.path.join(EJERCICIOS_DIR, nombre)
        ext = os.path.splitext(nombre)[1].lower()

        if ext == '.html':
            tipo = 'html'
        elif ext == '.json':
            tipo = 'json'
        elif ext == '.py':
            tipo = 'py'
        else:
            tipo = 'other'

        is_valid = True
        if tipo == 'json':
            is_valid = es_json_valido(full_path)

        titulo = os.path.splitext(nombre)[0]
        categoria = extraer_categoria(titulo)
        size = os.path.getsize(full_path)

        try:
            Resource.objects.create(
                title=titulo[:300],
                file_path=nombre,
                resource_type=tipo,
                category=categoria,
                file_size=size,
                is_valid=is_valid,
            )
            creados += 1
            if creados % 50 == 0:
                print('  Creados:', creados)
        except Exception as e:
            print('  ERROR con', nombre[:60], ':', e)
            saltados += 1

    print()
    print('=== RESULTADO ===')
    print('Creados:', creados)
    print('Saltados:', saltados)
    print('Total en BD:', Resource.objects.count())
    print()
    print('Validos:', Resource.objects.filter(is_valid=True).count())
    print('Invalidos:', Resource.objects.filter(is_valid=False).count())
    print()
    print('--- Por tipo ---')
    for tipo in ['html', 'json', 'py', 'other']:
        n = Resource.objects.filter(resource_type=tipo).count()
        print(' ', tipo, ':', n)
    print()
    print('--- Por categoria (top 10) ---')
    from django.db.models import Count
    cats = Resource.objects.values('category').annotate(n=Count('id')).order_by('-n')[:10]
    for c in cats:
        print(' ', c['category'], ':', c['n'])


if __name__ == '__main__':
    main()