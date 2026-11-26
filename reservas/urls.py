# reservas/urls.py
from django.urls import path

from . import views

app_name = "reservas"
urlpatterns = [
    # as_view() convierte la clase en una función que Django puede llamar
    path("", views.EspacioListView.as_view(), name="lista"),
    path("espacios/<int:pk>/", views.EspacioDetailView.as_view(), name="detalle"),
]
