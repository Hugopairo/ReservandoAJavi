# ruff: noqa: RUF012  (aviso de estilo; en el admin de Django es normal usar listas)
from django.contrib import admin

from .models import Espacio, Reserva


# [Guion, fase 6] Panel de administración de los espacios
# @admin.register hace que el modelo aparezca en /admin/
@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tipo", "aforo", "activo"]  # columnas de la tabla
    list_filter = ["tipo", "activo"]  # filtros del lateral
    search_fields = ["nombre"]  # el buscador busca por nombre


# [Guion, fase 6] Panel de administración de las reservas
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    # columnas de la tabla
    list_display = ["espacio", "fecha", "hora_inicio", "hora_fin", "usuario", "estado"]
    list_filter = ["estado", "espacio", "fecha"]  # filtros del lateral
    # usuario__username: los dos guiones bajos entran en el usuario para buscar por su nombre
    search_fields = ["motivo", "usuario__username"]
    # trae el espacio y el usuario en la misma consulta (menos consultas a la base de datos)
    list_select_related = ["espacio", "usuario"]
    readonly_fields = ["creada"]  # se ve en el formulario, pero no se puede editar
