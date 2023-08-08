"""
URL configuration for web1pato project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from web import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'estudiantes'


urlpatterns = [
     path('admin/', admin.site.urls),
    path('hola/', views.welcome_view, name='welcome'),  
    path('registro/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('dashboard/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),

    path('registro_estuiante/', views.solicitud_matricula, name='registro_estudiante'),


    path ('materia/', views.materia, name='materias'),

    path('formulario/', views.formulario_datos, name='formulario_datos'),
    path('display/', views.display_data, name='display_data'),
    path('download_data/', views.download_data, name='download_data'),
    path('actualizar/', views.actualizar_datos_estudiante, name='actualizar_datos_estudiante'),

       path('subir_pdf/', views.subir_pdf, name='subir_pdf'),
    path('eliminar_pdf/<int:pdf_id>/', views.eliminar_pdf, name='eliminar_pdf'),
    path('descargar/<int:pdf_id>/<str:version>/', views.descargar_version_pdf, name='descargar_version_pdf'),
    path('editar_pdf/<int:pdf_id>/', views.editar_pdf, name='editar_pdf'),
    path('descargar_pdf/<int:pdf_id>/', views.descargar_version_pdf, name='descargar_version_pdf'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)