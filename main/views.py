from django.shortcuts import render, redirect

from django.contrib import auth, messages

def main(request):
    message = messages.success(request, "Just Checking messages!")
    context = {
        "title": "Main Page",
        "message": message,
    }
    return render(request, "base.html", context)

def login_view(request):
    context = {
        "title": "Login",
    }
    return render(request, "login.html", context)

def signup(request):
    context = {
        "title": "Signup",
    }
    return render(request, "signup.html", context)

def logout(request):
    auth.logout(request)
    return redirect("login")