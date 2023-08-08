from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Agregar campos adicionales para el perfil del usuario si es necesario
    # Ejemplo: nombre, apellido, fecha de nacimiento, etc.

    def __str__(self):
        return self.user.username
    

    

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    semestre = models.IntegerField()

    def __str__(self):
        return self.nombre


    
GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
]

class DatosEstudiante(models.Model):
    foto = models.ImageField(upload_to='profile_photos/')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class DocumentoPDF(models.Model):
    nombre = models.CharField(max_length=100)
    archivo_pdf = models.FileField(upload_to='pdfs/')
    materia = models.CharField(max_length=100)
    version = models.CharField(max_length=20, null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre