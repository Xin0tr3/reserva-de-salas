from django.db import models

# Create your models here.
class Salas(models.Model):
    nombre_sala = models.CharField(max_length=100)
    numero_sala = models.PositiveIntegerField(default=1)
    capacidad_maxima = models.PositiveIntegerField(default=1)
    equipo_incluido = models.TextField()
    descripcion_sala = models.TextField()
    hora_minima = models.TimeField()
    hora_maxima= models.TimeField()

class Reservas(models.Model):
    estado_opciones = [
        ('CONFIRMADA', 'Confirmada'),
        ('PENDIENTE', 'Pendiente de aprobacion'),
        ('CANCELADA', 'Cancelada'),
    ]

    hora_inicio = models.DateTimeField()
    hora_termino = models.DateTimeField()
    nombre_reservante = models.CharField(max_length=255)
    departamento = models.CharField(max_length=100)
    email = models.EmailField()
    nombre_evento = models.CharField( max_length=100)
    descripcion_evento = models.TextField()
    equipamiento_extra = models.TextField()
    estado_reserva = models.CharField(max_length=15, choices=estado_opciones, default='PENDIENTE')
    codigo = models.CharField(max_length=50, unique=True, null=True, blank=False)
    rut = models.CharField(max_length=12,blank=False)
    sala_reservada = models.ForeignKey(Salas, on_delete=models.CASCADE)

