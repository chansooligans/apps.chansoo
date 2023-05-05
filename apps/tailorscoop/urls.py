from tailorscoop import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('/today/', views.today_story, name='today')
]