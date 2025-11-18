# forms.py - VERSIÓN CORREGIDA
from django import forms
from .models import Venta, ItemVenta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Reset, ButtonHolder, Field, HTML
from django.forms import inlineformset_factory

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        # ⚠️ IMPORTANTE: Solo campos que EXISTEN en el modelo Venta
        fields = ['codigo', 'cliente']  # ← ESTOS SON LOS ÚNICOS CAMPOS QUE DEBERÍAN ESTAR AQUÍ
        
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'codigo': 'Código de venta',
            'cliente': 'Cliente',
        }
        help_texts = {
            'codigo': 'Ingrese el código único para la venta.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()  # Usa FormHelper directo temporalmente
        self.helper.layout = Layout(
            Field("codigo"),
            Field("cliente"),
            ButtonHolder(
                Submit("submit", "Guardar", css_class="btn btn-success"),
                Reset("reset", "Limpiar", css_class="btn btn-outline-secondary"),
                HTML('<a href="{% url "ventas:listar_ventas" %}" class="btn btn-secondary">Cancelar</a>')
            )
        )


class ItemVentaForm(forms.ModelForm):
    class Meta:
        model = ItemVenta
        fields = ['producto', 'cantidad', 'precio_unitario']  # Estos campos SÍ están en ItemVenta
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Importante para formsets
        self.helper.layout = Layout(
            Field("producto"),
            Field("cantidad"),
            Field("precio_unitario"),
        )


VentaDetalleFormSet = inlineformset_factory(
    Venta,
    ItemVenta,
    form=ItemVentaForm,
    fields=['producto', 'cantidad', 'precio_unitario'],
    extra=1,
    can_delete=True
)