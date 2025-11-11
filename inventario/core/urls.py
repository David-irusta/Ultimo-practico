from django.urls import path, include
from . import views

app_name = "core"
urlpatterns = [
    path("LogueoExitoso/", views.LogueoExitosoView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout_message"),
]