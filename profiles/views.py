from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages


def index(request):
    return render(request, 'profiles/base.html')


def RegistrationFormView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('/')

    else:
        form = UserRegistrationForm()

    return render(request, 'profiles/register.html', {'form': form})


@login_required
def ProfileView(request):
    return render(request, 'profiles/profile.html')
