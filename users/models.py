from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLES = (
        ('client', 'Client'),
        ('assistant', 'Assistant'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES)
    credits = models.IntegerField(default=5)

    def __str__(self):
        return self.user.username