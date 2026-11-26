from django import forms

from .models import Espacio, Reserva


# Fase 8: ModelForm crea los campos y valida a partir del modelo Reserva
class ReservaForm(forms.ModelForm):
    # Meta: configuración del formulario
    class Meta:
        model = Reserva
        # Solo lo que rellena la persona (no elige ni 'usuario' ni 'estado')
        fields = ["espacio", "fecha", "hora_inicio", "hora_fin", "motivo"]
        # textos que se ven al lado de cada campo
        labels = {
            "hora_inicio": "Hora de inicio",
            "hora_fin": "Hora de fin",
        }
        # widgets: cómo se pinta cada campo (calendario y reloj del navegador)
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "hora_fin": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
        }

    # se ejecuta cada vez que se crea el formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # en el desplegable solo salen los espacios activos
        self.fields["espacio"].queryset = Espacio.objects.filter(activo=True)
