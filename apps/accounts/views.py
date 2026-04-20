from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm



def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print("FORM VALID ✅")
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = SignupForm()
        print(form.errors)  

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        
        # 1. Try to authenticate using username
        user = authenticate(request, username=identifier, password=password)
        
        # 2. If fails, try to authenticate using email
        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password.")
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully. See you soon!")
    return redirect('login')


def home_view(request):
    return render(request, 'home.html')

    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully. See you soon!")
    return redirect('login')


def home_view(request):
    return render(request, 'home.html')

