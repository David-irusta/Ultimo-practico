from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [
    path("lista-cliente", views.ClienteListView.as_view(), name="cliente_list"),
    path("crear/", views.ClienteCreateView.as_view(), name="crear_cliente"),
    path("detalle/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path("editar/<int:pk>/", views.ClienteUpdateView.as_view(), name="cliente_form"),
    path("eliminar/<int:pk>/", views.ClienteDeleteView.as_view(), name="cliente_confirm_delete"),
]
