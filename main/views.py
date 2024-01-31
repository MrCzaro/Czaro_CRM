from django.shortcuts import render, redirect

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from .models import User, USER_CHOICES

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
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        profession = request.POST.get("profession", "")
        email = request.POST.get("email", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        
        if first_name and last_name and email and password1 and password2 and profession:
            if password1 == password2:
                user = User.objects.create_user(first_name, last_name, email, password1, profession)
                messages.success(request, "Your account has been created. You can login.")
                return redirect("main:login")
            else:
                messages.error(request, "Your password do not match.")
        else: 
            messages.error(request, "Error while creating an account. Please provide a valid email address, name, and password.")                   
        
    context = {
        "title": "Signup",
        'USER_CHOICES': USER_CHOICES,
    }
    return render(request, "signup.html", context)

def logout_view(request):
    auth.logout(request)
    return redirect("main:login")