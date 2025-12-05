from django.urls import path
from .api import views as api_views

urlpatterns = [
    path('api/v1/salas/', api_views.SalaListCreateAPIView.as_view(), name='api-salas-disponibilidad'),
    path('api/v1/reservar/', api_views.ReservaCreateAPIView.as_view(), name='api-reserva-create'),
    path('api/v1/admin/reservas/', api_views.ReservaListaAdminAPIView.as_view(), name='api-lista-reserva-admin'),
    path('api/v1/admin/reservas/<str:codigo>/', api_views.ReservaDetallesAdminAPIView.as_view(), name='api-lista-detallada-admin')
]