from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book, BookLog
from Auth.models import User
from .serializers import BookSerializer, BookLogSerializer, UserSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post', 'patch'], permission_classes=[IsAdminUser])
    def issue(self, request, pk=None):
        book = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=400)
        user = get_object_or_404(User, pk=user_id)
        if book.isAvailable and book not in user.userbooklist.all():
            user.userbooklist.add(book)
            book.isAvailable = False
            book.save()
            BookLog.objects.create(user=user, book=book, action='borrow')
            return Response({'status': f'Book issued to {user.username}'})
        return Response({'error': 'Book not available or already borrowed by this user'}, status=400)

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

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user != user and not request.user.is_librarian:
            return Response({'error': 'Not authorized'}, status=403)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        return self.put(request, pk)

class BookPhotoUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        photo = request.data.get('book_photo')
        if not photo:
            return Response({'error': 'No photo uploaded'}, status=400)
        book.book_photo = photo
        book.save()
        return Response({'status': 'photo updated', 'photo_url': book.book_photo.url})

    def patch(self, request, pk):
        return self.put(request, pk)

class UserBorrowedBooksView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        books = user.userbooklist.all()
        return Response(BookSerializer(books, many=True).data)

class UserLogsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        logs = BookLog.objects.filter(user=user).order_by('-timestamp')
        return Response(BookLogSerializer(logs, many=True).data)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user != user and not request.user.is_librarian:
            return Response({'error': 'Not authorized'}, status=403)
        password = request.data.get('password')
        if not password or len(password) < 6:
            return Response({'error': 'Password must be at least 6 characters'}, status=400)
        user.password = make_password(password)
        user.save()
        return Response({'status': 'Password changed successfully'})

class LibrarianUsersBorrowedView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.filter(is_librarian=False)
        data = []
        for user in users:
            books = user.userbooklist.all()
            data.append({
                'user': UserSerializer(user).data,
                'borrowed_books': BookSerializer(books, many=True).data
            })
        return Response(data) 