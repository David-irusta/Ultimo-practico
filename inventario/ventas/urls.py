from django.urls import path
from . import views


app_name = 'ventas'

urlpatterns = [
    path('Listar-venta/', views.VentaListView.as_view(), name='venta_list'),
    path('Registrar-venta/<int:pk>/', views.VentaDetailView.as_view(), name='venta_detail'),
    path('Registrar-venta/nuevo/', views.VentaCreateView.as_view(), name='venta_form'),
]

