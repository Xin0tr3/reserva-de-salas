from django.urls import path, include
from .api import views as api_views
from django.shortcuts import render
from . import views

def cancelacion_view(request):
    return render(request, 'reservas/cancelar_reserva.html')

urlpatterns = [
    path('api/', include('reservas.api.urls')),
    path('cancelar-reserva', cancelacion_view, name='cancelacion'),
    path('reservas/gestionar/<str:codigo>/<str:accion>/', views.gestionar_reserva, name='web-gestionar-reserva')
]