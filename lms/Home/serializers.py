from rest_framework import serializers
from .models import Book, BookLog
from Auth.models import User
#respresentational state transfer

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book  # Tells Django which model to serialize
        fields = '__all__'  # Includes all fields from the Book model

# Serializer for the BookLog model (e.g., borrow/return logs)
class BookLogSerializer(serializers.ModelSerializer):
    # Instead of returning full user/book objects, use their __str__() representations
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = BookLog  # Serializing BookLog entries
        fields = '__all__'  # Include all fields (like user, book, timestamp, etc.)

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # This is your custom user model from the Auth app

        # We’re excluding sensitive or admin-related fields for safety and clarity
        exclude = [
            'password',          # We don’t want to expose password hash
            'last_login',        # Not necessary for normal user display
            'is_superuser',      # Internal admin flags
            'is_admin',
            'groups',
            'user_permissions'   # Permissions are mostly for internal access control
        ]
