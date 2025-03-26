from django.contrib.auth.models import AbstractUser
from django.db import models
from campus.models import Campus
from PIL import Image


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            output_size = (200, 200)
            if img.height > 200 or img.width > 200:
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username