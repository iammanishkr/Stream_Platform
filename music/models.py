from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    artist_image = models.ImageField(upload_to='artist_images/', null=True, blank=True)  # New field for artist image
    album = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='cover_images/')
    audio_file = models.FileField(upload_to='audio_files/')
    duration = models.CharField(max_length=10)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

