# reservas/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView

from .forms import ReservaForm
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
        contexto = super().get_context_data(**kwargs)

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


# Fase 8: crear una nueva reserva (protegida con inicio de sesión)
# LoginRequiredMixin va a la izquierda: comprueba la sesión antes que la vista
class ReservaCreateView(LoginRequiredMixin, CreateView):
    # formulario que se muestra y se valida (ejecuta también el clean() del modelo)
    form_class = ReservaForm
    template_name = "reservas/reserva_form.html"
    # adónde ir al guardar; lazy porque las rutas aún no están cargadas
    success_url = reverse_lazy("reservas:mias")

    # solo se llama si el formulario es válido
    def form_valid(self, form):
        # la reserva queda a nombre de quien ha iniciado sesión, antes de guardarla
        form.instance.usuario = self.request.user
        # la clase padre guarda y redirige; el estado queda en pendiente (por defecto)
        return super().form_valid(form)


# Fase 8: listado de reservas del usuario actual
class MisReservasView(LoginRequiredMixin, ListView):
    template_name = "reservas/mis_reservas.html"
    context_object_name = "reservas"

    def get_queryset(self):
        # solo mis reservas; select_related trae el espacio en la misma consulta
        return Reserva.objects.filter(usuario=self.request.user).select_related(
            "espacio"
        )
