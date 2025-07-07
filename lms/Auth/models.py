from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from Home.models import Book

class UserManager(BaseUserManager):
    """
    Custom manager for User model where email and username are required.
    """
    def create_user(self, username, email, password=None, userdob=None, profile_pic=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            userdob=userdob,
            profile_pic=profile_pic
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, userdob=None, profile_pic=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            userdob=userdob,
            profile_pic=profile_pic
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the library system with extended fields.
    Inherits from PermissionsMixin for Django admin compatibility.
    """
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    userdob = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    userbooklist = models.ManyToManyField(Book, blank=True, related_name='borrowed_by')
    wishlist = models.ManyToManyField(Book, blank=True, related_name='wishlisted_by')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def bookdues(self):
        return self.userbooklist.all()
