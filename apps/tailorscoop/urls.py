from tailorscoop import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('/today/', views.today_story, name='today'),
    path('/unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
]