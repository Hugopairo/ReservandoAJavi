# reservas/views.py
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Espacio, Reserva


# Fase 7: lista de espacios (ListView muestra varios objetos)
class ListaEspacios(ListView):
    template_name = "reservas/lista.html"  # plantilla que se usa
    context_object_name = "espacios"  # nombre con el que la plantilla recibe la lista

    # qué espacios salen: solo los activos
    def get_queryset(self):
        return Espacio.objects.filter(activo=True)


# Fase 7: ficha de un espacio (DetailView muestra uno, buscado por el pk de la URL)
class DetalleEspacio(DetailView):
    model = Espacio
    template_name = "reservas/detalle.html"
    context_object_name = "espacio"

    # manda datos extra a la plantilla
    def get_context_data(self, **kwargs):
        # primero, lo que ya prepara la clase padre
        contexto = super().get_context_data(
            **kwargs
        )

        # reservas de este espacio (self.object)
        contexto["reservas"] = (
            Reserva.objects.filter(
                fecha__gte=timezone.localdate(),  # de hoy en adelante
                espacio=self.object,
                estado=Reserva.Estado.CONFIRMADA,  # solo las confirmadas
            )
            .select_related("usuario")  # trae el usuario en la misma consulta
            .order_by("fecha")  # ordenadas por fecha
        )

        return contexto
