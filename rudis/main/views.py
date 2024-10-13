# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .bakcends import EmailBackend
# from models import CustomUser
from .models import *

# Define a view function for the home page
def home(request):
    return render(request, 'main/home.html')

# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not CustomUser.objects.filter(email=email).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        # Authenticate the user with the provided username and password
        user = CustomUser(email=email, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            EmailBackend.authenticate(request, email, password)
            return redirect('/')

    # Render the login page template (GET request)
    return render(request, 'main/login.html')

# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Check if a user with the provided username already exists
        user = CustomUser.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        if password != password2:
            messages.info(request, "Так не пойдет, давай чтоб пароли были похожи хотя бы")
            return redirect('/register/')

        try:
            validate_email(email)
            print()
        except ValueError as exc:
            messages.info(request, f"Так давай дуй нормальную почту: {exc}")
            return redirect('/register/')
        # Create a new User object with the provided information
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')

    # Render the registration page template (GET request)
    return render(request, 'main/register.html')
