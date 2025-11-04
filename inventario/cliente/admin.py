from django.contrib import admin
from .models import Cliente

<<<<<<< HEAD
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'numero_documento', 'email', 'telefono', 'direccion']
    list_filter = ['email']
    search_fields = ['nombre', 'email', 'numero_documento']
=======
# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'numero_documento', 'email']
    list_filter = ['numero_documento']
    search_fields = ['nombre', 'apellido', 'numero_documento']
>>>>>>> 1e66e3f (Apps en admin)
