from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from .models import Trainer, Stock, Abonnement


@cache_page(180)
def show_info(request):
    return render(request, 'Gym_at_the_Moscow/home_page.html')


def abon_func(request):
    ab = Abonnement.objects.order_by('time')
    return render(request, 'Gym_at_the_Moscow/ab_page.html', {'ab': ab})


def hall_func(request):
    return render(request, 'Gym_at_the_Moscow/hall_page.html')

@cache_page(120)
def trainer_func(request):
    trainer = Trainer.objects.order_by('full_name')
    return render(request, 'Gym_at_the_Moscow/trainer.html', {'trainer': trainer})


def stock_func(request):
    stock = Stock.objects.order_by('date_ac')
    return render(request, 'Gym_at_the_Moscow/stock_page.html', {'stock': stock})


def slug_func(request, slug_trainer):
    train = get_object_or_404(Trainer, slug=slug_trainer)
    return render(request, 'Gym_at_the_Moscow/full_name.html', {'train': train})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, "Gym_at_the_Moscow/register.html", {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, "Gym_at_the_Moscow/login.html", {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
