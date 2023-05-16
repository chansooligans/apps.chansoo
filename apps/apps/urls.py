"""apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from twilioapp import views as twilioviews
from django.http import HttpResponseRedirect
from . import views as apps_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
    path("centraljersey", include("centraljersey.urls")),
    path("sms", twilioviews.receive_sms),
    path("tailoredscoop/", include("tailorscoop.urls")),
    path("demo/", apps_views.demo, name='demo'),
    path("", RedirectView.as_view(url="/tailoredscoop/")),
]
