from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from .forms import RegisterForm, PostForm, ProfileForm, UserForm
from django.contrib.auth import login, authenticate
from .models import Post, Profil, User, Friend
from slugify import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        'post': get_object_or_404(Post, slug=slug, rodzaj=kat),
        'posts': posts,
        'user': request.user})


def profile(request, name):
    posts = Post.objects.filter(autor=request.user)
    return render_to_response('Profile.html', {'profil': get_object_or_404(User, username=name),
                                               'user': request.user,
                                               'posts': posts})


def wpis(request, kat):
    cat = Post.objects.filter(rodzaj=kat)
    return render_to_response("Kategoria.html", {'user': request.user,
                                                 'kategoria': cat})

@login_required
def usun(request, post_pk):
    qw = Post.objects.get(pk=post_pk)
    qw.delete()
    return redirect('/profile/' + request.user.username)

@login_required
def utworz(request):
    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            pst = form.save(commit=False)
            pst.autor = user
            sl = form.cleaned_data.get('tytul')
            pst.slug = slugify(sl, to_lower=True)
            pst.save()
            return redirect('profile', name=user.username)
    else:
        form = PostForm()
    return render(request, 'Dodaj.html', {'form': form})


@login_required
def edytuj(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = user
            post.slug = slugify(form.cleaned_data.get('tytul'), to_lower=True)
            post.save()
            return redirect('profile', name=user.username)
    else:
        form = PostForm(instance=post)
        return render(request, 'Dodaj.html', {'form': form})


def ustawienia(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        prof_form = ProfileForm(request.POST, instance=user.profil)
        print(user_form.errors)
        print(prof_form.errors)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            print("Wszystko ok!")
            return redirect('profile', name=user.username)
    else:
        user_form = UserForm(instance=user)
        prof_form = ProfileForm(instance=user.profil)

    return render(request, "Ustawienia.html", {'user_form': user_form, 'prof_form': prof_form})


@login_required
def znajomi(request):
    users = User.objects.exclude(id=request.user.id)
    friend, created = Friend.objects.get_or_create(current_user=request.user)
    other = Friend.objects.exclude(current_user=request.user)
    obs = other.filter(friends__username__contains=request.user.username)

    fr = friend.friends.all()
    return render(request, 'Znajomi.html', {'users': users, 'friends': fr, 'followers': obs})


@login_required
def znaj_akcje(request, action, pk):
    new_friend = User.objects.get(pk=pk)
    if action == 'add':
        Friend.dodawanie(request.user, new_friend)
    elif action == 'remove':
        Friend.usuwanie(request.user, new_friend)
    return redirect('znajomi')


@login_required
def znaj_prof(request, pk):
    user = request.user
    friend = User.objects.get(pk=pk)
    posts = Post.objects.filter(autor=friend)
    return render(request, 'ProfInfo.html', {"user": user, "friend": friend, "posts": posts})
