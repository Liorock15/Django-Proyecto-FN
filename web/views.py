
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import UserRegistrationForm, UserLoginForm, UserPasswordResetForm, UserChangePasswordForm
from .forms import EstudianteForm
from .models import Estudiante
from .forms import DatosEstudianteForm
from .models import DatosEstudiante
from django.http import HttpResponse
from django.http import HttpResponse
import io
from django.http import HttpResponse, Http404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import DatosEstudiante
from .forms import DocumentoPDFForm
from .models import DocumentoPDF
from django.shortcuts import get_object_or_404, redirect
from .models import DocumentoPDF

def welcome_view(request):
    return redirect('register')  # Redirige a la página de registro

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'inicio/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirecciona a la página de bienvenida después del inicio de sesión exitoso
            else:
                messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
    else:
        form = UserLoginForm()
    return render(request, 'inicio/login.html', {'form': form})

@login_required
def home_view(request):
    # Vista de bienvenida para usuarios autenticados
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Vistas de recuperación y cambio de contraseña proporcionadas por Django
password_reset_view = PasswordResetView.as_view(form_class=UserPasswordResetForm)
password_reset_done_view = PasswordResetDoneView.as_view()
password_reset_confirm_view = PasswordResetConfirmView.as_view(form_class=UserChangePasswordForm)
password_reset_complete_view = PasswordResetCompleteView.as_view()


def solicitud_matricula(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EstudianteForm()

    estudiantes = Estudiante.objects.all()
    return render(request, 'pag/registro_alumno.html', {'form': form, 'estudiantes': estudiantes})



def materia(request):
    return render(request, 'pag/materia.html')

def formulario_datos(request):
    if request.method == 'POST':
        form = DatosEstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('display_data')
    else:
        form = DatosEstudianteForm()

    return render(request, 'pag/formulario.html', {'form': form})

def display_data(request):
    data_estudiante = DatosEstudiante.objects.last()
    return render(request, 'pag/display_data.html', {'datos_estudiante': data_estudiante})

def download_data(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="datos_estudiante.pdf"'

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    datos_estudiante = DatosEstudiante.objects.last()

    # Add the data to the PDF
    y = 700
    pdf.drawString(100, y, "Nombre: {}".format(datos_estudiante.nombre))
    y -= 20
    pdf.drawString(100, y, "Apellido: {}".format(datos_estudiante.apellido))
    y -= 20
    pdf.drawString(100, y, "Correo electrónico: {}".format(datos_estudiante.email))
    y -= 20
    pdf.drawString(100, y, "Teléfono: {}".format(datos_estudiante.telefono))
    y -= 20
    pdf.drawString(100, y, "Fecha de Nacimiento: {}".format(datos_estudiante.fecha_nacimiento))
    y -= 20
    pdf.drawString(100, y, "Género: {}".format(datos_estudiante.get_genero_display()))
    y -= 20
    pdf.drawString(100, y, "Dirección: {}".format(datos_estudiante.direccion))
    y -= 20
    pdf.drawString(100, y, "Ciudad: {}".format(datos_estudiante.ciudad))
    y -= 20
    pdf.drawString(100, y, "País: {}".format(datos_estudiante.pais))

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response.write(buffer.getvalue())
    return response


def actualizar_datos_estudiante(request):
    datos_estudiante = DatosEstudiante.objects.last()

    if request.method == 'POST':
        form = DatosEstudianteForm(request.POST, instance=datos_estudiante)
        if form.is_valid():
            form.save()
            return redirect('formulario_datos')
    else:
        form = DatosEstudianteForm(instance=datos_estudiante)

    return render(request, 'pag/formulario.html', {'form': form})

def subir_pdf(request):
    if request.method == 'POST':
        form = DocumentoPDFForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subir_pdf')
    else:
        form = DocumentoPDFForm()
    pdfs = DocumentoPDF.objects.all()
    return render(request, 'pag/subir_pdf.html', {'form': form, 'pdfs': pdfs})


def eliminar_pdf(request, pdf_id):
    pdf = get_object_or_404(DocumentoPDF, id=pdf_id)
    pdf.delete()
    return redirect('subir_pdf')

def descargar_version_pdf(request, pdf_id):
    try:
        pdf = get_object_or_404(DocumentoPDF, id=pdf_id)
        file_path = pdf.archivo_pdf.path
        with open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf.nombre}.pdf"'
            return response
    except DocumentoPDF.DoesNotExist:
        raise Http404("El archivo PDF no existe.")

    
def editar_pdf(request, pdf_id):
    pdf = get_object_or_404(DocumentoPDF, id=pdf_id)

    if request.method == 'POST':
        form = DocumentoPDFForm(request.POST, request.FILES, instance=pdf)
        if form.is_valid():
            form.save()
            return redirect('subir_pdf')
    else:
        form = DocumentoPDFForm(instance=pdf)

    return render(request, 'pag/editar_pdf.html', {'form': form, 'pdf': pdf})