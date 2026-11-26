# reservas/views.py
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Espacio, Reserva  # el punto significa "de esta misma aplicación"


# [Guion, fase 7] Lista de espacios. ListView ya sabe mostrar una lista
class EspacioListView(ListView):
    template_name = "reservas/lista.html"  # plantilla que se usa
    context_object_name = "espacios"  # nombre con el que la plantilla recibe la lista

    # decide qué objetos salen en la lista: solo los activos
    def get_queryset(self):
        return Espacio.objects.filter(activo=True)


# [Guion, fase 7] Ficha de un espacio. DetailView lo busca con el pk de la URL
# y, si no existe, responde con un error 404
class EspacioDetailView(DetailView):
    model = Espacio  # modelo en el que busca
    template_name = "reservas/detalle.html"
    context_object_name = "espacio"  # nombre del objeto en la plantilla

    # sirve para mandar datos extra a la plantilla, además del espacio
    def get_context_data(self, **kwargs):
        # primero cojo los datos que ya prepara DetailView
        contexto = super().get_context_data(**kwargs)
        # próximas reservas de este espacio (self.object es el espacio mostrado)
        contexto["reservas"] = self.object.reservas.filter(
            estado=Reserva.Estado.CONFIRMADA,  # solo las confirmadas
            fecha__gte=timezone.localdate(),  # de hoy en adelante (gte: mayor o igual)
        ).select_related("usuario")  # trae el usuario en la misma consulta
        return contexto
