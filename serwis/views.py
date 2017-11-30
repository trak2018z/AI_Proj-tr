from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, authenticate

# Create your views here.


def index(request):
    return render(request, 'Index.html', {})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.errors)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profil.lokacja = form.cleaned_data.get('location')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            print('UPS cos poszlo nie tak!')

    else:
        form = RegisterForm()
    return render(request, 'registration/Rejestracja.html', {'form': form})
