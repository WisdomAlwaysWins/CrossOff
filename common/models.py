from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, serialize=True)
    name = models.CharField(blank=False, null=False, max_length=100)