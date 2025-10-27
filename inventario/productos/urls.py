from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='producto_list'),
    path('nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_form'),
    path('<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_confirm_delete'),
    path('<int:pk>/movimiento/', views.MovimientoStockCreateView.as_view(), name='producto_movimiento_form'),
    path('<int:pk>/ajustar-stock/', views.AjusteStockView.as_view(), name='ajuste_stock_form'),
    path('stock-bajo/', views.StockBajoListView.as_view(), name='stock_bajo_list'),
]