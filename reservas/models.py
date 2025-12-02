from django.db import models

# Create your models here.
class salas(models.Model):
    nombre_sala = models.CharField
    numero_sala = models.PositiveIntegerField
    capacidad_maxima = models.PositiveIntegerField
    equipo_incluido = models.CharField
    descripcion_sala = models.CharField
    hora_minima = models.TimeField
    hora_maxima= models.TimeField

class reservas(models.Model):
    fecha_reserva = models.DateField
    hora_inicio = models.TimeField
    hora_termino = models.TimeField
    nombre_reservante = models.CharField
    departamente = models.CharField
    email = models.EmailField
    nombre_evento = models.CharField
    descripcion_evento = models.CharField
    equipamiento_extra = models.CharField
    confirmacion = models.BooleanField
    codigo = models.CharField
    rut = models.CharField

