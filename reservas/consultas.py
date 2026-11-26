from django.db.models import Count, Q

from .models import Espacio, Reserva


# [Guion, fase 7] Ocupación de los espacios en una fecha
def ocupacion(fecha):
    # devuelve los espacios activos con el número de reservas confirmadas de ese día
    return (
        Espacio.objects.filter(activo=True)  # solo los espacios activos
        # annotate añade a cada espacio un dato calculado
        .annotate(
            reservas_confirmadas=Count(
                "reservas",  # cuenta las reservas de cada espacio
                # la condición va dentro de Count: así los espacios con 0 siguen saliendo
                # reservas__ sirve para llegar desde el espacio a los campos de sus reservas
                filter=Q(
                    reservas__fecha=fecha,
                    reservas__estado=Reserva.Estado.CONFIRMADA,
                ),
            )
        )
        # el - ordena de mayor a menor; si empatan, por nombre
        .order_by("-reservas_confirmadas", "nombre")
    )
