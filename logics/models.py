from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# \products of the club


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    votes = models.ManyToManyField(default=0, unique=True)
    price = models.DecimalField(max_digits=2)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=False)
    updated_at = models.DateTimeField(auto_now=True)


# club creation
class ClubGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        User, blank=True, related_name="clubs", unique=True)
    is_active = models.BooleanField(default=False)
    collection = models.ManyToManyField(
        Product, blank=True, related_name="Products")
    created_at = models.DateTimeField(auto_now_add=True, auto_created=False)
    updated_at = models.DateTimeField(auto_now=True)
    group_master = models.ForeignKey(User, on_delete=models.DO_NOTHING)
