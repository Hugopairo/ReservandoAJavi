import copy

# el error de Django se renombra para no confundirlo con el de DRF
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Espacio, Reserva


# Fase 9: un serializador convierte entre objetos del modelo y JSON
class EspacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = ["id", "nombre", "tipo", "aforo", "activo"]


# serializador de reservas: además aplica las reglas de la fase 5
class ReservaSerializer(serializers.ModelSerializer):
    # campos extra de solo lectura; source dice de dónde sale el dato
    espacio_nombre = serializers.CharField(source="espacio.nombre", read_only=True)
    usuario = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Reserva
        fields = [
            "id",
            "espacio",
            "espacio_nombre",
            "usuario",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "motivo",
            "estado",
            "creada",
        ]
        # se ven en las respuestas, pero se ignoran si el cliente los envía
        read_only_fields = ["estado", "creada"]

    # attrs son los datos recibidos, ya convertidos a sus tipos
    def validate(self, attrs):
        # si es una modificación se usa una copia, para no tocar la original
        if self.instance:
            reserva = copy.copy(self.instance)
        else:
            reserva = Reserva()

        # se ponen los datos recibidos en la reserva de prueba
        for campo, valor in attrs.items():
            setattr(reserva, campo, valor)

        # DRF no llama a clean() solo: se llama aquí (horas, espacio activo, solapes)
        try:
            reserva.clean()
        except DjangoValidationError as error:
            # el solape es un error general (sin error_dict): sale en non_field_errors
            raise serializers.ValidationError(
                error.message_dict if hasattr(error, "error_dict") else error.messages
            )

        return attrs
