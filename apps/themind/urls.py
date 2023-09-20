from themind import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='themind'),
    path("room/<str:room_name>/", views.room, name="room"),
    path('reset', views.reset, name='reset'),
    path('delete-all-numbers/', views.delete_all_numbers, name='delete_all_numbers'),
    path('set-room-name/', views.set_room_name, name='set_room_name'),
]