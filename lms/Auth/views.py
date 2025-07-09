from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User  # Use the custom User model
from django.contrib import messages
import logging

logger = logging.getLogger(__name__) #logger created for the current module name loggername =yourapp.views

# Create your views here.

def login(request):
    if request.method == 'POST':   #post method for creation adn update of data
        email = request.POST.get('username')  # This is actually the email field in your form and returns none if missing
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist: #if no email registered
            messages.error(request, 'User with this email does not exist.')
            logger.debug(f"User with email '{email}' does not exist.") #for the debug log
            return render(request, "login.html")

        if not user_obj.check_password(password): #if wrong password  
            messages.error(request, 'Password does not match for this user.')
            logger.debug(f"Password does not match for user with email '{email}'.")
            return render(request, "login.html")


        auth_login(request, user_obj)   #once user stays logged in
        logger.debug(f"User with email '{email}' logged in successfully.") #will store log in even reopening the page
        return redirect('/')
    return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    return render(request, "register.html")

def logout(request):
    if request.method == 'POST':
        auth_logout(request) #remove user session data from server either unliked or invalidated
        messages.success(request, 'You have been logged out.')
        return redirect('home')
    # For GET or other methods, just redirect to home
    return redirect('home')