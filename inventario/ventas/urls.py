from django.urls import path
from . import views


app_name = 'ventas'

urlpatterns = [
    path('Listar-venta/', views.VentaListView.as_view(), name='venta_list'),
    path('nuevo/', views.VentaCreateView.as_view(), name='venta_create'),
    path('<int:pk>/editar/', views.VentaUpdateView.as_view(), name='venta_form'),
    path('<int:pk>/detalle/', views.VentaDetailView.as_view(), name='venta_detail'),
    path('<int:pk>/eliminar/', views.VentaDeleteView.as_view(), name='venta_delete'),
    path('<int:pk>/pdf/', views.VentaPDFView.as_view(), name='venta_pdf'),
]

