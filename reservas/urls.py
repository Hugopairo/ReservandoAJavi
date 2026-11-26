# reservas/urls.py
from django.urls import path

from . import views

app_name = "reservas"
urlpatterns = [
    # as_view() convierte la clase en una vista que Django puede llamar
    path("", views.ListaEspacios.as_view(), name="lista"),
    # <int:pk> recoge el número del espacio de la dirección
    path("espacios/<int:pk>/", views.DetalleEspacio.as_view(), name="detalle"),
]
