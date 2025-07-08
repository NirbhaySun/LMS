from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, BookLog
from django.core.paginator import Paginator
from django.db import models
from Auth.decorators import librarian_required
from .forms import BookForm
from Auth.models import User

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
        if action == 'wishlist' and not in_wishlist:
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

@librarian_required
def librarian_dashboard(request):
    books = Book.objects.all().order_by('-created_at')
    borrowed_books = Book.objects.filter(isAvailable=False)
    return render(request, 'librarian/dashboard.html', {
        'books': books,
        'borrowed_books': borrowed_books,
    })

@librarian_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('librarian_dashboard')
    else:
        form = BookForm()
    return render(request, 'librarian/add_edit_book.html', {'form': form, 'action': 'Add'})

@librarian_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    users = User.objects.filter(is_active=True, is_librarian=False)
    issued_user_id = None
    was_borrowed = not book.isAvailable
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        issued_user_id = request.POST.get('issue_to_user')
        if form.is_valid():
            old_is_available = book.isAvailable
            form.save()
            # Handle return if isAvailable was set to True
            if not old_is_available and form.cleaned_data['isAvailable']:
                borrowers = User.objects.filter(userbooklist=book)
                for borrower in borrowers:
                    borrower.userbooklist.remove(book)
                    BookLog.objects.create(user=borrower, book=book, action='return')
                book.isAvailable = True
                book.save()
            # Issue book if user selected and book is available
            if issued_user_id and book.isAvailable:
                user = get_object_or_404(User, pk=issued_user_id)
                if book not in user.userbooklist.all():
                    user.userbooklist.add(book)
                    book.isAvailable = False
                    book.save()
                    BookLog.objects.create(user=user, book=book, action='borrow')
                    messages.success(request, f'Book issued to {user.username}!')
            messages.success(request, 'Book updated successfully!')
            return redirect('librarian_dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'librarian/add_edit_book.html', {'form': form, 'action': 'Edit', 'users': users, 'book': book})

@librarian_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('librarian_dashboard')
    return render(request, 'librarian/confirm_delete.html', {'book': book})

@librarian_required
def return_book(request, book_id, user_id):
    book = get_object_or_404(Book, pk=book_id)
    user = get_object_or_404(User, pk=user_id)
    if book in user.userbooklist.all():
        user.userbooklist.remove(book)
        book.isAvailable = True
        book.save()
        BookLog.objects.create(user=user, book=book, action='return')
        messages.success(request, f'Book "{book.book_name}" marked as returned for {user.username}.')
    return redirect('librarian_dashboard')

@librarian_required
def notifications(request):
    logs = BookLog.objects.select_related('user', 'book').order_by('-timestamp')[:50]
    return render(request, 'librarian/notifications.html', {'logs': logs})

@librarian_required
def assign_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    users = User.objects.filter(is_active=True)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        if book.isAvailable and book not in user.userbooklist.all():
            user.userbooklist.add(book)
            book.isAvailable = False
            book.save()
            # Log as 'user borrowed book' for notifications
            BookLog.objects.create(user=user, book=book, action='borrow')
            messages.success(request, f"{user.username} borrowed {book.book_name}.")
            return redirect('librarian_dashboard')
        else:
            messages.error(request, 'Book is not available or already borrowed by this user.')
    return render(request, 'librarian/assign_book.html', {'book': book, 'users': users})
