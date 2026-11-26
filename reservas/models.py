from django.conf import settings
from django.core.exceptions import ValidationError
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
        constraints = [  # noqa: RUF012 es para quitar el erro bueno silenciarlo q es topesao
            models.CheckConstraint(
                condition=models.Q(hora_fin__gt=models.F("hora_inicio")),
                name="reserva_fin_posterior_inicio",
            )
        ]

    def __str__(self):
        return (
            f"{self.espacio} {self.fecha:%d/%m/%Y} "
            f"{self.hora_inicio:%H:%M}-{self.hora_fin:%H:%M}"
        )

    # [Guion, fase 5] Detectar solapamientos entre reservas
    def solapes(self):
        # Devuelve True si hay otra reserva confirmada que pisa este horario
        return (
            # Busca en la base de datos; las condiciones se cumplen todas a la vez
            Reserva.objects.filter(
                espacio=self.espacio,  # mismo espacio
                fecha=self.fecha,  # mismo día
                estado=Reserva.Estado.CONFIRMADA,  # solo las confirmadas
                hora_inicio__lt=self.hora_fin,  # empieza antes de que yo termine
                hora_fin__gt=self.hora_inicio,  # termina después de que yo empiece
            )
            .exclude(pk=self.pk)  # no me comparo conmigo (al editar una reserva)
            .exists()  # True si queda alguna, False si no queda ninguna
        )

    # [Guion, fase 5] Reglas que debe cumplir una reserva
    def clean(self):
        # Se ejecuta al validar (full_clean), no al hacer save().
        # El primer raise detiene el método.

        # Regla 1: la hora de fin debe ser posterior a la de inicio
        # (antes se comprueba que las dos horas existan)
        if self.hora_fin and self.hora_inicio and self.hora_fin <= self.hora_inicio:
            raise ValidationError(
                {"hora_fin": "La hora de fin debe ser posterior a la de inicio."}
            )

        # Regla 2: el espacio tiene que estar activo
        # espacio_id va primero: si no hay espacio, no se accede a self.espacio
        if self.espacio_id and not self.espacio.activo:
            raise ValidationError(
                {"espacio": "El espacio no está disponible para reservas."}
            )

        # Regla 3: una reserva no cancelada no puede pisar a una confirmada
        # solapes() va al final: solo consulta la base de datos si todo lo anterior se cumple
        if (
            self.espacio_id
            and self.fecha
            and self.hora_inicio
            and self.hora_fin
            and self.estado != Reserva.Estado.CANCELADA
            and self.solapes()
        ):
            # Error general: no pertenece a un solo campo
            raise ValidationError(
                "El espacio ya tiene una reserva confirmada que se solapa con ese horario."
            )
