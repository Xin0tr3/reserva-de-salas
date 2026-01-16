from django.db import models

# Create your models here.
class Salas(models.Model):
    pisos_opciones = [
        ('PISO 1', 'Piso 1'),
        ('PISO 2', 'Piso 2'),
    ]

    nombre_sala = models.CharField(max_length=100)
    numero_sala = models.PositiveIntegerField(default=1)
    capacidad_maxima = models.PositiveIntegerField(default=1)
    equipo_incluido = models.TextField()
    descripcion_sala = models.TextField()
    hora_minima = models.TimeField()
    hora_maxima= models.TimeField()
    piso_sala = models.CharField(max_length=15, choices=pisos_opciones, default='PISO 1')

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
    nombre_evento = models.CharField(max_length=100)
    descripcion_evento = models.TextField()
    equipamiento_extra = models.TextField(blank=True)
    estado_reserva = models.CharField(max_length=15, choices=estado_opciones, default='PENDIENTE')
    codigo = models.CharField(max_length=50, unique=True, null=True, blank=False)
    rut = models.CharField(max_length=12,blank=False)
    sala_reservada = models.ForeignKey(Salas, on_delete=models.CASCADE)

class Invitados(models.Model):
    rol_opciones = [
        ('FUNCIONARIO', 'Funcionario'),
        ('ACADEMICO', 'Academico'),
        ('ALUMNO', 'Alumno'),
    ]
    sexo_opciones = [
        ('HOMBRE', 'Hombre'),
        ('MUJER', 'Mujer'),
        ('SIN ESPECIFICAR', 'Sin especificar')
    ]
    nombre_invitado = models.CharField(max_length=100)
    apellidos_invitado = models.CharField(max_length=100)
    rol = models.CharField(max_length=15, choices=rol_opciones, default='FUNCIONARIO')
    carrera = models.CharField(max_length=100, blank=True)
    facultad = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=15, choices=sexo_opciones, default='SIN ESPECIFICAR')
    codigo_reserva = models.ForeignKey(Reservas, on_delete=models.CASCADE)