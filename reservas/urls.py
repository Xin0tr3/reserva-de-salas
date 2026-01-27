from django.urls import path, include
from .api import views as api_views
from django.shortcuts import render
from . import views
from django.contrib.auth.decorators import login_required

def cancelacion_view(request):
    return render(request, 'reservas/cancelar_reserva.html')

def reservacion_view(request):
    return render(request, 'reservas/reservar_salas.html')

@login_required
def admin_inicio_view(request):
    return render(request, 'reservas/admin_inicio.html')

@login_required
def gestion_salas_view(request):
    return render(request, 'reservas/gestion_salas.html')

@login_required
def gestion_usuarios_view(request):
    return render(request, 'reservas/gestion_usuarios.html')

@login_required
def gestion_reservas_view(request):
    return render(request, 'reservas/gestion_reservas.html')



urlpatterns = [
    path('api/', include('reservas.api.urls')),
    path('login/', views.login_vista, name='login'),
    path('reservar-sala/', reservacion_view, name='reservacion'),
    path('cancelar-reserva/', cancelacion_view, name='cancelacion'),
    path('reservas/gestionar/<str:codigo>/<str:accion>/', views.gestionar_reserva, name='web-gestionar-reserva'),
    path('admin-inicio/', admin_inicio_view, name='admin-inicio'),
    path('admin-inicio/admin-salas/', gestion_salas_view, name='admin-salas'),
    path('admin-inicio/admin-usuarios/', gestion_usuarios_view, name='admin-usuarios'),
    path('admin-inicio/admin-reservas/', gestion_reservas_view, name='admin-reservas')
]