from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


from .models import User, USER_CHOICES

@login_required(login_url="/login/")
def main(request):
    # Main view, requires authentication. If not authenticated, redirects to login.
    context = {
        "title": "Main Page",
    }
    return render(request, "base.html", context)


# Authentication
def login_view(request):
    # Handles user login.
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("patient:index")
        else:
            messages.error(request, "Invalid login credentials. Please try again.")

    context = {
        "title": "Login",
    }
    return render(request, "login.html", context)

def signup_view(request):
    # Handles user signup. Validates input and creates a new user if conditions are met.
    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        profession = request.POST.get("profession", "")
        email = request.POST.get("email", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        
        if (
            first_name
            and last_name
            and email
            and password1
            and password2
            and profession
        ):
            if User.objects.filter(email=email).exists():
                messages.error(request,"An account with this email already exists.")
            elif password1 == password2:
                try:
                    validate_email(email)
                    User.objects.create_user(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password1,
                        profession=profession,
                    )
                    messages.success(request, "Your account has been created. You can login.")
                    return redirect("main:login")
                except ValidationError:
                     messages.error(request, "Please provide a valid email address.")
            else:
                messages.error(request, "Your password do not match.")
        else:
            messages.error(
                request,
                "Error while creating an account. Please provide a valid email address, name, and password.",
            )
         

    context = {
        "title": "Signup",
        "USER_CHOICES": USER_CHOICES,
    }
    return render(request, "signup.html", context)


def logout_view(request):
    # Logs out the user and redirects to the login page.
    auth.logout(request)
    return redirect("main:login")
