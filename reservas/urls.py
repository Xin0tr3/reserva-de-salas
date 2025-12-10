from django.urls import path
from .api import views as api_views
from . import views

urlpatterns = [
    path('api/v1/salas/', api_views.SalaDisponiblesAPIView.as_view(), name='api-salas-disponibilidad'),
    path('api/v1/reservar/', api_views.ReservaCreateAPIView.as_view(), name='api-reserva-create'),
    path('api/v1/admin/reservas/', api_views.ReservaListaAdminAPIView.as_view(), name='api-lista-reserva-admin'),
    path('api/v1/admin/reservas/<str:codigo>/', api_views.ReservaDetallesAdminAPIView.as_view(), name='api-lista-detallada-admin'),
    path('api/v1/admin/salas/', api_views.SalasCreacionAPIView.as_view(), name='api-salas-creacion'),
    path('api/v1/admin/salas/<str:pk>', api_views.SalasModificacionELiminacionAPIView.as_view(), name='api_salas-modificacion'),
    path('reservas/gestionar/<str:codigo>/<str:accion>/', views.gestionar_reserva, name='web-gestionar-reserva')
]