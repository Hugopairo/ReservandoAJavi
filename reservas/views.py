# reservas/views.py
from django.shortcuts import get_object_or_404, render

from .models import Espacio  # el punto significa "de esta misma aplicación"


# tarea 5
def lista(request):
    # pongo filtrer para que pasen los que cumplen
    espacios = Espacio.objects.filter(activo=True)
    # "espacios" es el nombre con el que la plantilla recibe los datos
    return render(request, "reservas/lista.html", {"espacios": espacios})


# fase 5 Detalle de un espacio leído de la base de datos
def detalle(request, pk):
    # pk = número del espacio, viene de la URL (/espacios/3/ -> pk = 3)
    # Busco el espacio con ese pk; si no existe, sale un error 404
    espacio = get_object_or_404(Espacio, pk=pk)
    # Mando el espacio a la plantilla con el nombre "espacio"
    return render(request, "reservas/detalle.html", {"espacio": espacio})
