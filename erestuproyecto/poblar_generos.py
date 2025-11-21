# poblar_generos.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

from fitness.models import Genero

def poblar_generos():
    generos = [
        'Masculino',
        'Femenino', 
        'Prefiero no decirlo',
        'Otro'
    ]
    
    for nombre in generos:
        Genero.objects.get_or_create(genero=nombre)
    
    print("✅ Tabla de géneros poblada exitosamente!")

if __name__ == '__main__':
    poblar_generos()