from themind import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='themind'),
    path('reset', views.reset, name='reset'),
    path('delete-all-numbers/', views.delete_all_numbers, name='delete_all_numbers'),
]