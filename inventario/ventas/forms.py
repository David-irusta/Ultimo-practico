from django import forms
from .models import Venta, ItemVenta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import inlineformset_factory

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['codigo', 'cliente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'codigo': 'Codigo de venta',
            'cliente': 'Cliente',
            'fecha': 'Fecha de la venta',
            'total': 'Precio total de la venta',
        }
        help_texts = {
            'codigo': 'Ingrese el codigo unico para la venta.'
        }
        def __init__(self, *args, **kwargs):
            super(VentaForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Guardar Venta'))
        

class ItemVentaForm(forms.ModelForm):
    class Meta:
        model = ItemVenta
        fields = ['producto', 'cantidad', 'precio_unitario']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio',
        }

        def save(self, commit=True):
            item_venta = super().save(commit=False)
            item_venta.precio_unitario = item_venta.producto.precio_venta
            if commit:
                item_venta.save()
            return item_venta

        def __init__(self, *args, **kwargs):
            super(ItemVentaForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Agregar Item'))
VentaDetalleFormSet = inlineformset_factory(
    Venta,
    ItemVenta,
    form=ItemVentaForm,
    extra=1,
    can_delete=False
)


