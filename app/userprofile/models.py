from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Profiles", default="Default/avatar.png")
    bio = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return str(self.user)
