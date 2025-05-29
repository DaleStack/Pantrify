from django.urls import path
from .views import recipe, home_view

urlpatterns = [
    path("chat/", recipe, name="generate_recipe"),
    path("", home_view, name="home_view"),
]
