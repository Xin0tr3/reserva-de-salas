from django.contrib import admin
from .models import Salas , Reservas
# Register your models here.

@admin.register(Salas)
class SalaAdmin(admin.ModelAdmin):
    #Estos son los campos que se muestran en la lista de salas

    list_display = (
        'nombre_sala',
        'numero_sala',
        'capacidad_maxima'
    )

#campos por los que se puede buscar
search_fields = ('nombre_sala', 'numero_sala', 'descripcion_sala')
#filtros laterales
list_filter = ('capacidad_maxima')

@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_reservante',
        'sala_reservada',
        'fecha_reserva',
        'rut',
        'estado_reserva',
        'codigo'
    )
list_filter = ('estado_reserva', 'sala_reservada', 'hora_inicio')

search_fields = (
    'nombre_reservante',
    'email',
    'nombre_evento',
    'codigo'
)

readonly_fields = ('codigo')