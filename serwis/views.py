from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from .models import Post, Profil, User

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
    else:
        posts = Post.objects.all()[:3]
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


def post(request, kat, slug):
    posts = Post.objects.all()
    return render_to_response('Post.html', {
        'post': get_object_or_404(Post, slug=slug),
        'posts': posts,
        'user': request.user})


def profile(request, name):
    posts = Post.objects.filter(autor=request.user)
    return render_to_response('Profile.html', {'profil': get_object_or_404(User, username=name),
                                               'user': request.user,
                                               'posts': posts})


def wpis(request, cat):
    kat = Post.objects.filter(rodzaj=cat)
    return render_to_response("Kategoria.html", {'user': request.user,
                                                 'kategoria': kat})


def usun(request, post_pk):
    qw = Post.objects.get(pk=post_pk)
    qw.delete()
    return redirect('/profile/' + request.user.username)
