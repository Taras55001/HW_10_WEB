from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


from .forms import RegistrationForm, LoginForm, AuthorForm, PostForm
from .models import Author, Quote


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quotes:root')
    else:
        form = LoginForm(request)
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')


def add_author_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:root')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            user = request.user
            quote = Quote.objects.create(
                quote=form.cleaned_data['quote'],
                author=form.cleaned_data['author'],
                user=user,
            )
            quote.tags.set(tags)

            return redirect('quotes:root')
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'quotes/add_post.html', {'form': form})
