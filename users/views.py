from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You've logged in successfully...")
            return redirect("home")
        else:
            messages.error(request, "Credentials error!")
            return redirect("home")

    return render(request, "index.html")

def user_logout(request):
    logout(request)
    messages.success(request, "You've been logged out successfully...")
    return redirect("home")

def user_register(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "passwords didn't match...")
            return redirect("home")
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered...")
            return redirect("home")
        
        user = User.objects.create_user(username=email, password=password)
        user.save()
        messages.success(request, "You've registered successfully...")
        return redirect("home")
    
    return render(request, "index.html")