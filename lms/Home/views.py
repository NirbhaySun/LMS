from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book

# Create your views here.

@login_required(login_url='login')
def home(request):
    """
    Render the main home page of the library system. Only accessible to logged-in users.
    Shows the latest books added.
    """
    latest_books = Book.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'latest_books': latest_books})
