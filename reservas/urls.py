from django.urls import path, include
from .api import views as api_views
from . import views

urlpatterns = [
    path('api/', include('reservas.api.urls')),
    path('reservas/gestionar/<str:codigo>/<str:accion>/', views.gestionar_reserva, name='web-gestionar-reserva')
]