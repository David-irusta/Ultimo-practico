from django import forms
from .models import Venta, ItemVenta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import inlineformset_factory

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['codigo', 'cliente', 'fecha']

ItemVentaFormSet = inlineformset_factory(
    Venta,
    ItemVenta,
    fields=('producto', 'cantidad', 'precio_unitario'),
    extra=1,
    can_delete=True
)

'''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar Venta'))

class ItemVentaForm(forms.ModelForm):
    class Meta:
        model = ItemVenta
        fields = ['producto', 'cantidad', 'precio_unitario']

ItemVentaFormSet = inlineformset_factory(
    Venta, ItemVenta, form=ItemVentaForm,
    extra=1, can_delete=True, min_num=1, validate_min=True'''
