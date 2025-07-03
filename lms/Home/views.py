from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from django.core.paginator import Paginator
from django.db import models

# Create your views here.

@login_required(login_url='login')
def home(request):
    """
    Render the main home page of the library system. Only accessible to logged-in users.
    Shows the latest books added.
    """
    query = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '')
    books = Book.objects.all().order_by('-created_at')

    if query:
        books = books.filter(
            models.Q(book_name__icontains=query) |
            models.Q(book_author__icontains=query) |
            models.Q(book_genre__icontains=query)
        )
    if genre:
        books = books.filter(book_genre=genre)

    paginator = Paginator(books, 5)  # 5 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'query': query,
        'genre': genre,
        'genre_choices': Book.GENRE_CHOICES,
    })

@login_required(login_url='login')
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    in_my_books = book in user.userbooklist.all()
    in_wishlist = book in user.wishlist.all()
    is_borrowed = not book.isAvailable
    is_borrowed_by_user = in_my_books

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'borrow' and book.isAvailable and not in_my_books:
            user.userbooklist.add(book)
            book.isAvailable = False
            book.save()
            messages.success(request, 'Book added to your books!')
            return redirect('book_detail', book_id=book.book_id)
        elif action == 'wishlist' and not in_wishlist:
            user.wishlist.add(book)
            messages.success(request, 'Book added to your wishlist!')
            return redirect('book_detail', book_id=book.book_id)
        elif action == 'remove_wishlist' and in_wishlist:
            user.wishlist.remove(book)
            messages.success(request, 'Book removed from your wishlist.')
            return redirect('book_detail', book_id=book.book_id)

    # Recalculate after possible POST
    in_my_books = book in user.userbooklist.all()
    in_wishlist = book in user.wishlist.all()
    is_borrowed = not book.isAvailable
    is_borrowed_by_user = in_my_books

    return render(request, 'book_detail.html', {
        'book': book,
        'in_my_books': in_my_books,
        'in_wishlist': in_wishlist,
        'is_borrowed': is_borrowed,
        'is_borrowed_by_user': is_borrowed_by_user,
    })
