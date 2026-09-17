#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Parche temporal: usar Django 5 del PythonPortable_Django5
# (mientras el antivirus bloquea el python.exe en esa carpeta)
sys.path.insert(0, r'E:\PythonPortable_Django5\Lib\site-packages')
# Asegurar que el paquete del proyecto este en el path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduplatform.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


