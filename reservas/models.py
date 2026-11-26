from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Espacio(models.Model):
    class Tipo(models.TextChoices):
        AULA = "aula", "Aula"
        LABORATORIO = "laboratorio", "Laboratorio"
        SALON = "salon", "Salón de actos"
        PISTA = "pista", "Pista deportiva"

    nombre = models.CharField(max_length=80, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    aforo = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]  # noqa: RUF012

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("reservas:detalle", args=[self.pk])


class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    espacio = models.ForeignKey(
        Espacio, on_delete=models.PROTECT, related_name="reservas"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservas"
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PENDIENTE
    )
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora_inicio"]  # noqa: RUF012

    def __str__(self):
        return (
            f"{self.espacio} {self.fecha:%d/%m/%Y} "
            f"{self.hora_inicio:%H:%M}-{self.hora_fin:%H:%M}"
        )
