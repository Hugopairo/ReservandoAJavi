from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # rutas de usuarios que Django trae hechas: cuentas/login/, cuentas/logout/...
    path("cuentas/", include("django.contrib.auth.urls")),
    path("", include("reservas.urls")),
]
