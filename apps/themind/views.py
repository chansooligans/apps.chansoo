# views.py
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import RandomNumber
import random

def home(request):

    generated_pairs = RandomNumber.objects.all()
    all_numbers = set(range(1, 101))
    remaining_numbers = all_numbers - {pair.value1 for pair in generated_pairs} - {pair.value2 for pair in generated_pairs}
    
    if len(remaining_numbers) < 2:
        context = {"message": "Not enough numbers remaining to generate a unique pair!"}
    else:
        # Randomly select two unique numbers from the remaining numbers
        number1, number2 = random.sample(remaining_numbers, 2)
        RandomNumber.objects.create(value1=number1, value2=number2)
        context = {"number1": number1, "number2": number2}

    return render(request, 'themind/home.html', context)

def reset(request):
    return render(request, 'themind/reset.html')

@require_POST
def delete_all_numbers(request):
    RandomNumber.objects.all().delete()
    return redirect('reset') 