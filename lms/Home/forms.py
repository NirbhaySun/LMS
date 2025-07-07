from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_name', 'book_author', 'book_genre', 'book_photo', 'isAvailable']
        widgets = {
            'book_genre': forms.Select(),
        } 