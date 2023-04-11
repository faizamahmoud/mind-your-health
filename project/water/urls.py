# path/, name of view, string name of route
from django.urls import path
from .views import WaterIntakeView


urlpatterns = [
    path('water/', WaterIntakeView.as_view(), name='water-intake'),
]
