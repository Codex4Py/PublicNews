from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news_posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']


class Comment(models.Model):
    post = models.ForeignKey(NewsPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  # Corrected to use the custom user model
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post.title}'

    class Meta:
        ordering = ['-created_at']


class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook-f', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin-in', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='other')
    url = models.URLField(max_length=200)
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


# Custom User Model for Login & Signup System

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
