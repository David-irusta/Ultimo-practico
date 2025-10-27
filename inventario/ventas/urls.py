from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path('carrito/', views.VentaListView.as_view(), name='venta_list'),
    path('<int:pk>/detalle/', views.VentaDetailView.as_view(), name='venta_detail'),
    path('crear/', views.VentaCreateView.as_view(), name='venta_form'),
]
