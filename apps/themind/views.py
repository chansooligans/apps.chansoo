from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from .models import RandomNumber
import random

@never_cache
def home(request):

    return render(request, 'themind/home.html')

@never_cache
def room(request, room_name):

    generated_pairs = RandomNumber.objects.all()
    all_numbers = set(range(1, 101))
    remaining_numbers = all_numbers - {pair.value1 for pair in generated_pairs} - {pair.value2 for pair in generated_pairs}
    
    if len(remaining_numbers) < 2:
        context = {"message": "Not enough numbers remaining to generate a unique pair!", "room_name": room_name}
    else:
        # Randomly select two unique numbers from the remaining numbers
        number1, number2 = random.sample(remaining_numbers, 2)
        RandomNumber.objects.create(value1=number1, value2=number2, room_name=room_name)
        context = {"number1": number1, "number2": number2, "room_name":room_name}

    return render(request, 'themind/room.html', context)

def delete_all_numbers(request, room_name):
    context = {"room_name": room_name}
    RandomNumber.objects.filter(room_name=room_name).delete()
    return render(request, 'themind/reset.html', context)

@never_cache
def set_room_name(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        request.session["room_name"] = room_name
        return redirect(f'/themind/room/{room_name}')
    return HttpResponse("Invalid request.", status=400)