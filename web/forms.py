from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Estudiante
from .models import DatosEstudiante
from .models import DocumentoPDF



class UserRegistrationForm(UserCreationForm):
    # Aquí puedes personalizar los campos del formulario de registro si es necesario
    # Ejemplo: agregar un campo de correo electrónico adicional
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserPasswordResetForm(PasswordResetForm):
    # Personaliza el formulario de recuperación de contraseña si es necesario
    pass

class UserChangePasswordForm(SetPasswordForm):
    # Personaliza el formulario de cambio de contraseña si es necesario
    pass




class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'carrera', 'semestre']


class DatosEstudianteForm(forms.ModelForm):
    class Meta:
        model = DatosEstudiante
        fields = '__all__'

class DatosEstudianteForm(forms.ModelForm):
    class Meta:
        model = DatosEstudiante
        fields = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'genero', 'direccion', 'ciudad', 'pais', 'foto']

class DocumentoPDFForm(forms.ModelForm):
    class Meta:
        model = DocumentoPDF
        fields = ['nombre', 'archivo_pdf', 'materia']