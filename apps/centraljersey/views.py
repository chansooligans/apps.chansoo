# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def leaflet(request):
    return render(request, 'centraljersey/leaflet.html')
