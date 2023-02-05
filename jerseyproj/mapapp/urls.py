from mapapp import views
from django.urls import path

urlpatterns = [
    path('', views.leaflet, name='leaflet'),
]