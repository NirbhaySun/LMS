from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api_views

router = DefaultRouter()
router.register(r'books', api_views.BookViewSet, basename='book')
router.register(r'users', api_views.UserViewSet, basename='user')
router.register(r'logs', api_views.BookLogViewSet, basename='booklog')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/wishlist/', api_views.WishlistView.as_view(), name='user-wishlist'),
    path('librarian/assign/', api_views.AssignBookView.as_view(), name='assign-book'),
    path('librarian/return/', api_views.ReturnBookView.as_view(), name='return-book'),
] 