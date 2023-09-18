from tailorscoop import views
from django.urls import path

urlpatterns = [
    path('themind/', views.home, name='home'),
]