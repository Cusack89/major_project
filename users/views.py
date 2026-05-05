from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, EmailAuthenticationForm


def login_view(request):
    ## 1) Check is user is already logged in
    if request.user.is_authenticated:
        return redirect("my_app:dashboard")

    if request.method == "POST":
        ## 2) GET username and password
        username = request.POST.get("username")
        password = request.POST.get("password")

        ## 3) Authenticate user
        user = authenticate(request, username=username, password=password)

        ## 4) Send to dashboard page
        if user is not None:
            login(request, user)
            return redirect("/my_app/")  
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required(login_url='users:login')
def user(request):
    return render(request, "my_app/home.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('users:login')