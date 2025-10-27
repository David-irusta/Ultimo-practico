from django import forms
from .models import Cliente
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'numero_documento', 'email', 'telefono', 'direccion']

    def __init__ (self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar Cliente'))