from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from .models import Post

# Create your views here.


def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.errors)

        if form.is_valid():
            form.save()
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


def post(request, slug):
    posts = Post.objects.all()
    return render_to_response('Post.html', {
        'post': get_object_or_404(Post, slug=slug),
        'posts': posts})