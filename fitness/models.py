from django.db import models
from django.contrib.auth.models import User
from django.db import models
import python_avatars as pa
# from django.db.models.signals import post_save
# from django.dispatch import receiver
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_svg = models.TextField(blank=True)
    
    def generar_avatar(self):
        """Genera y guarda un avatar para el usuario"""
        avatar_svg = pa.Avatar.random().render()
        self.avatar_svg = avatar_svg
        self.save()

class Genero(models.Model):
    id_genero  = models.AutoField(db_column='idGenero', primary_key=True) 
    genero     = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return str(self.genero)




class Datos(models.Model):
    PERFIL_CHOICES = [
        ('entrenador', 'Entrenador'),
        ('estudiante', 'Estudiante'),
        
    ]
    
    rut = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=20)
    apellido_paterno = models.CharField(max_length=20)
    apellido_materno = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(blank=False, null=False) 
    id_genero = models.ForeignKey('Genero', on_delete=models.CASCADE, db_column='idGenero')  
    telefono = models.CharField(max_length=45)
    peso = models.FloatField()
    altura = models.DecimalField(max_digits=3, decimal_places=2)
    email = models.EmailField(unique=True, max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)  
    perfil = models.CharField(max_length=15, choices=PERFIL_CHOICES, default='estudiante', null=True, blank=True)
    activo = models.IntegerField()
    # Nueva relación con el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.nombre) + " " + str(self.apellido_paterno)

    class Meta:      
        ordering = ['rut']

    def es_administrador(self):
        # El administrador principal se identifica por username y password específicos
        return self.user.username == 'admin' and self.user.check_password('admin123')
        receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs): se descomentara el viernes
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
class VidaSaludable(models.Model):
    vegetal_favorito = models.CharField(max_length=100)
    peso = models.FloatField()  # Aquí se corrige el error
    ejercicio_favorito = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.vegetal_favorito} - {self.ejercicio_favorito}"
