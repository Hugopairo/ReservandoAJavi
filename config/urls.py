from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from reservas.api import EspacioViewSet, ReservaViewSet

# fase 9: el router crea solo las direcciones de cada ViewSet
router = DefaultRouter()
# basename hace falta porque el ViewSet usa get_queryset() y no queryset
router.register("espacios", EspacioViewSet, basename="espacio")
router.register("reservas", ReservaViewSet, basename="reserva")

urlpatterns = [
    path("admin/", admin.site.urls),
    # rutas de usuarios que Django trae hechas: cuentas/login/, cuentas/logout/...
    path("cuentas/", include("django.contrib.auth.urls")),
    # fase 10: recibe usuario y contraseña (POST) y devuelve el token
    path("api/token/", obtain_auth_token, name="api-token"),
    # direcciones de la API
    path("api/", include(router.urls)),
    # entrar y salir desde las páginas web de la API
    path("api-auth/", include("rest_framework.urls")),
    path("", include("reservas.urls")),
]
