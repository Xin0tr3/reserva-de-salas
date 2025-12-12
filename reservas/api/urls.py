from django.urls import path
from . import views

urlpatterns = [
    path('v1/salas/', views.SalaDisponiblesAPIView.as_view(), name='api-salas-disponibilidad'),
    path('v1/reservar/', views.ReservaCreateAPIView.as_view(), name='api-reserva-create'),
    path('v1/admin/reservas/', views.ReservaListaAdminAPIView.as_view(), name='api-lista-reserva-admin'),
    path('v1/admin/reservas/<str:codigo>/', views.ReservaDetallesAdminAPIView.as_view(), name='api-lista-detallada-admin'),
    path('v1/admin/salas/', views.SalasCreacionAPIView.as_view(), name='api-salas-creacion'),
    path('v1/admin/salas/<str:pk>', views.SalasModificacionELiminacionAPIView.as_view(), name='api_salas-modificacion'),
]