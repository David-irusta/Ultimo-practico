from django.contrib import admin
from .models import Venta

# Register your models here.
<<<<<<< HEAD
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'fecha', 'total']
    list_filter = ['fecha', 'cliente']
    search_fields = ['codigo', 'cliente__nombre', 'cliente__apellido']
=======
#@admin.register(Venta)
>>>>>>> c866dbf (Models de ventas)
