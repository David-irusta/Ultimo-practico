from django.contrib import admin
from .models import Venta

# Register your models here.
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha', 'total']
    list_filter = ['fecha']
    search_fields = ['cliente_nombre', 'cliente_email']