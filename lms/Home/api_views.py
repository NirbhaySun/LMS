from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book, BookLog
from Auth.models import User
from .serializers import BookSerializer, BookLogSerializer, UserSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookLog.objects.all().order_by('-timestamp')
    serializer_class = BookLogSerializer

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        books = user.wishlist.all()
        return Response(BookSerializer(books, many=True).data)
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        book_id = request.data.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        user.wishlist.add(book)
        return Response({'status': 'added to wishlist'})
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        book_id = request.data.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        user.wishlist.remove(book)
        return Response({'status': 'removed from wishlist'})

class AssignBookView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        user = get_object_or_404(User, pk=user_id)
        book = get_object_or_404(Book, pk=book_id)
        if book.isAvailable and book not in user.userbooklist.all():
            user.userbooklist.add(book)
            book.isAvailable = False
            book.save()
            BookLog.objects.create(user=user, book=book, action='borrow')
            return Response({'status': f'{user.username} borrowed {book.book_name}'})
        return Response({'error': 'Book not available or already borrowed'}, status=400)

class ReturnBookView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        user = get_object_or_404(User, pk=user_id)
        book = get_object_or_404(Book, pk=book_id)
        if book in user.userbooklist.all():
            user.userbooklist.remove(book)
            book.isAvailable = True
            book.save()
            BookLog.objects.create(user=user, book=book, action='return')
            return Response({'status': f'{user.username} returned {book.book_name}'})
        return Response({'error': 'Book not borrowed by user'}, status=400) 