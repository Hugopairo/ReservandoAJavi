from datetime import date

from django.db.models import ProtectedError
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .consultas import ocupacion
from .models import Espacio, Reserva
from .permissions import EsPersonalOSoloLectura, EsPropietarioOSoloLectura
from .serializers import EspacioSerializer, ReservaSerializer


# Fase 9: un ModelViewSet ya trae listar, ver, crear, modificar y borrar
class EspacioViewSet(viewsets.ModelViewSet):
    serializer_class = EspacioSerializer
    # fase 10: cualquiera lee; solo el personal crea, modifica o borra
    permission_classes = [EsPersonalOSoloLectura]

    # qué espacios devuelve la API, según los filtros de la dirección
    def get_queryset(self):
        consulta = Espacio.objects.all()

        # query_params son los datos de detrás de ? ; si no llegan valen None
        tipo = self.request.query_params.get("tipo")
        activo = self.request.query_params.get("activo")

        if tipo:
            consulta = consulta.filter(tipo=tipo)

        # llega como texto: la comparación lo convierte en True o False
        if activo is not None:
            consulta = consulta.filter(activo=(activo == "true"))

        return consulta

    # se sobrescribe el borrado para controlar un error
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        # tiene reservas (on_delete=PROTECT): se responde 409 en vez de un 500
        except ProtectedError:
            return Response(
                {"detail": "El espacio tiene reservas y no se puede borrar."},
                status=status.HTTP_409_CONFLICT,
            )

    # acción extra en /api/espacios/ocupacion/ ; detail=False: no lleva id
    @action(detail=False, url_path="ocupacion")
    def ocupacion_del_dia(self, request):
        fecha_texto = request.query_params.get("fecha")
        if not fecha_texto:
            return Response(
                {"detail": "Falta el parámetro fecha (AAAA-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # fecha mal escrita: ValidationError de DRF, que responde 400
        try:
            fecha = date.fromisoformat(fecha_texto)
        except ValueError:
            raise serializers.ValidationError(
                {"fecha": "Formato de fecha no válido (AAAA-MM-DD)."}
            )

        # reutiliza ocupacion() de la fase 7 y la convierte en lista de diccionarios
        return Response(
            [
                {
                    "id": espacio.id,
                    "nombre": espacio.nombre,
                    "reservas_confirmadas": espacio.reservas_confirmadas,
                }
                for espacio in ocupacion(fecha)
            ]
        )


# API de reservas
class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    # fase 10: se exigen los dos: identificarse y, para escribir, ser el propietario
    permission_classes = [IsAuthenticated, EsPropietarioOSoloLectura]

    def get_queryset(self):
        # select_related trae espacio y usuario en la misma consulta
        consulta = Reserva.objects.select_related("espacio", "usuario")

        fecha_texto = self.request.query_params.get("fecha")
        espacio = self.request.query_params.get("espacio")
        estado = self.request.query_params.get("estado")

        # tres if separados: los filtros se pueden combinar
        if fecha_texto:
            try:
                fecha = date.fromisoformat(fecha_texto)
            except ValueError:
                raise serializers.ValidationError(
                    {"fecha": "Formato de fecha no válido (AAAA-MM-DD)."}
                )
            consulta = consulta.filter(fecha=fecha)

        if espacio:
            # comprobar que es un número evita un error 500
            if not espacio.isdigit():
                raise serializers.ValidationError(
                    {"espacio": "El identificador del espacio debe ser un número."}
                )
            consulta = consulta.filter(espacio_id=espacio)

        if estado:
            consulta = consulta.filter(estado=estado)

        return consulta

    # al crear, el usuario es el identificado, no el que envíe el cliente
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
