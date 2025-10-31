from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'numero_documento', 'email', 'telefono', 'direccion']
    list_filter = ['email']
    search_fields = ['nombre', 'email', 'numero_documento']
