from django.db import models

# Create your models here.

class Book(models.Model):
    """
    Model representing a book in the library.
    """
    GENRE_CHOICES = [
        ("Fiction", "Fiction (Novels, stories, drama, literary fiction)"),
        ("Non-Fiction", "Non-Fiction (Essays, journalism, real-life topics, how-to books)"),
        ("Science & Technology", "Science & Technology (Physics, biology, programming, engineering, mathematics)"),
        ("History & Politics", "History & Politics (Historical events, government, wars, biographies of leaders)"),
        ("Children & Young Adult", "Children & Young Adult (Books for kids, teens, fantasy for younger readers)"),
        ("Religion & Philosophy", "Religion & Philosophy (Spiritual texts, beliefs, ethics, thought systems)"),
        ("Education & Reference", "Education & Reference (Textbooks, guides, dictionaries, academic materials)"),
    ]
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_genre = models.CharField(max_length=40, choices=GENRE_CHOICES)
    isAvailable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # For latest books
    book_photo = models.ImageField(upload_to='book_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.book_name} by {self.book_author}"
