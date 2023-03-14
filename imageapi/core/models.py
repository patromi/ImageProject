import uuid
from datetime import datetime

import pytz
from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from rest_framework_api_key.crypto import KeyGenerator
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager
from users.models import ImageUser as User

class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    resolution = models.CharField(max_length=20)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=None,null=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('obraz-detail', args=[str(self.id)])

    def is_expired(self):
        if self.expired_at is None:
            return False
        return datetime.now(pytz.timezone('UTC')) > self.expired_at
