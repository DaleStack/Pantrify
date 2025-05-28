from django.urls import path
from .views import recipe

urlpatterns = [
    path("chat/", recipe, name="generate_recipe"),
]
