from django import forms
from django.forms import inlineformset_factory
from .models import Reservas, Invitados

# Definición de ReservaForm
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reservas
        # Aquí pones los campos que quieres que el usuario llene
        fields = [
            'hora_inicio', 'hora_termino', 'nombre_reservante', 
            'departamento', 'email', 'nombre_evento', 
            'descripcion_evento', 'equipamiento_extra', 'rut', 'sala_reservada'
        ]

# Definición de InvitadosFormSet
# Esto crea la conexión entre la Reserva (padre) e Invitados (hijos)
InvitadosFormSet = inlineformset_factory(
    Reservas,      # Modelo Padre
    Invitados,     # Modelo Hijo
    fields=(       # Campos que el invitado debe llenar
        'nombre_invitado', 'apellidos_invitado', 
        'rol', 'carrera', 'facultad', 'sexo'
    ),
    extra=1,       # Cuántos formularios vacíos aparecen por defecto
    can_delete=True # Permite marcar un invitado para borrarlo
)