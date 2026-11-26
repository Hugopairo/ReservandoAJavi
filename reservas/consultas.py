from django.db.models import Count, Q

from .models import Espacio


# Fase 7: ocupación de los espacios en una fecha
def ocupacion(fecha):
    return (
        Espacio.objects.filter(activo=True)  # solo los espacios activos
        # annotate añade a cada espacio un dato calculado
        .annotate(
            reservas_confirmadas=Count(
                "reservas",  # cuenta las reservas de cada espacio
                # la condición va dentro de Count: así los espacios con 0 siguen saliendo
                filter=Q(
                    reservas__fecha=fecha,
                    reservas__estado="confirmada",
                ),
            )
        )
        # el - ordena de más a menos; si empatan, por nombre
        .order_by("-reservas_confirmadas", "nombre")
    )
