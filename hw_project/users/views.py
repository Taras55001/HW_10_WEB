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


def generate_quote(author_name):
    prompt = f"Generate a quote by {author_name}: "
    response = openai.Completion.create(
        engine="text-davinci-002",  # Use the appropriate GPT-3 engine
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
        stop=["\n"]
    )
    quote = response['choices'][0]['text'].strip()
    return quote

def quote_generator(request, author_id):
    author = Author.objects.get(pk=author_id)
    quote = generate_quote(author.name)
    return render(request, 'quote.html', {'quote': quote})
