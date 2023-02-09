from django.db import models
from django.conf import settings
# Create your models here.
# \products of the club

# not added the votes mode, in a different way but with a different method


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    vote_count = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class MemberVote(models.Model):
    vote_product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


# club creation
class ClubGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="clubs")
    is_active = models.BooleanField(default=False)
    collection = models.ManyToManyField(
        Product, blank=True, related_name="Products")
    created_at = models.DateTimeField(auto_now_add=True, auto_created=False)
    updated_at = models.DateTimeField(auto_now=True)
    group_master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name
