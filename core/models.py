from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from cloudinary.models import CloudinaryField

class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        if not email:
            raise ValueError('User must have an email')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() 

    USERNAME_FIELD = 'email'


class Ingredients(models.Model):
    name = models.CharField(max_length=255)
    qty = models.IntegerField()
    unit = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} {self.qty} {self.unit}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class InstructionSet(models.Model):
    prerequisite = models.TextField(blank=True)

    def __str__(self):
        return self.prerequisite


class Step(models.Model):
    step_no = models.IntegerField()
    description = models.TextField()
    instruction_set = models.ForeignKey(InstructionSet, related_name='steps', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    time = models.IntegerField()
    servings = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_public = models.BooleanField()
    ingredients = models.ManyToManyField(Ingredients)
    category = models.ManyToManyField(Category)
    instruction_set = models.OneToOneField(InstructionSet, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='recipes')
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name

    def likes_count(self):
        return self.likes.count()


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    detail = models.TextField()

    def __str__(self):
        return self.detail

    
class Group(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owner_group'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    recipes = models.ManyToManyField(Recipe)
    users = models.ManyToManyField(User, related_name='group')

    def __str__(self):
        return self.name
    