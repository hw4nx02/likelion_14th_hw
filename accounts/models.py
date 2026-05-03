from django.contrib.auth.models import User
from django.db import models
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    age = models.IntegerField(null=True, blank=True)
    major = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return self.nickname
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            image = Image.open(self.profile_image.path)
            max_size = (300, 300)
            image.thumbnail(max_size)
            image.save(self.profile_image.path)