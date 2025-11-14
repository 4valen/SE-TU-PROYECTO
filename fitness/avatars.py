import python_avatars as pa
import random

def generar_avatar_aleatorio():
    """Genera un avatar completamente aleatorio"""
    return pa.Avatar.random().render()

def generar_avatar_para_usuario(username):
    """Genera un avatar consistente basado en el username"""
    # Usar el hash del username para hacerlo determinístico
    random.seed(hash(username))
    
    avatar = pa.Avatar.random()
    return avatar.render()