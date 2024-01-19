from django.shortcuts import render, redirect

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from .models import User

@login_required(login_url="/login/")
def main(request):
    context = {
        "title": "Main Page",
    }
    return render(request, "base.html", context)

# Authentication
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(request, username=email, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect("main:index")
        else:
            messages.error(request, "Invalid login credentials. Please try again." )
        
            
    context = {
        "title": "Login",
    }
    return render(request, "login.html", context)

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        
        if name and email and password1 and password2:
            if password1 == password2:
                user = User.objects.create_user(name, email, password1)
                messages.success(request, "Your account has been created. You can login.")
                return redirect("main:login")
            else:
                messages.error(request, "Your password do not match.")
        else: 
            messages.error(request, "Error while creating an account. Please provide a valid email address, name, and password.")                   
        
    context = {
        "title": "Signup",
    }
    return render(request, "signup.html", context)

def logout_view(request):
    auth.logout(request)
    return redirect("main:login")