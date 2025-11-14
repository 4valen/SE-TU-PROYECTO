
        
from django import forms
from .models import Datos  # Asegúrate de importar tus modelos correctamente

class VidaSaludableForm(forms.ModelForm):
    class Meta:
        model = Datos  # Ajusta esto según tu modelo real
        fields = "__all__" # Ajusta los campos según tu modelo
