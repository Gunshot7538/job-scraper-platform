
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
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
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignupForm()
        print(form.errors)  

    return render(request, 'signup.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')

