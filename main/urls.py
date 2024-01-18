from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.main, name="name"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    
]