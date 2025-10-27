from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path('Carrito/', views.VentaListView.as_view(), name='venta_list'),
    path('Detalle/<int:pk>/', views.VentaDetailView.as_view(), name='venta_detail'),
    path('Crear/', views.VentaCreateView.as_view(), name='venta_form'),   
]
