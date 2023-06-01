from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
# \products of the club

# not added the votes mode, in a different way but with a different method


class Product(models.Model):
    # defining the location of the file
    def upload_location(instance, filename):
        return 'product/{filename}'.format(filename=filename)

    product_mage = models.ImageField(
        _("Image"), upload_to=upload_location, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    vote_count = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=65, decimal_places=2)
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
    def upload_location(instance, filename):
        return 'club/{filename}'.format(filename=filename)

    name = models.CharField(max_length=255)
    description = models.TextField()
    subscription = models.DecimalField(
        max_digits=65, decimal_places=2, default="0.00")
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="clubs")
    is_active = models.BooleanField(default=False)
    collection = models.ManyToManyField(
        Product, blank=True, related_name="Products")
    club_image = models.ImageField(
        _("Image"), upload_to=upload_location, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=False)
    updated_at = models.DateTimeField(auto_now=True)
    group_master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def get_members(self):
        return ClubhouseMember.objects.filter(club=self)

    def __str__(self) -> str:
        return self.name


class RequestToJoinGroup(models.Model):
    STATUS_CHOICES = (
        ('APPROVED', 'APPROVED'),
        ('PENDING', 'PENDING'),
        ('REJECTED', 'REJECTED'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    club_group = models.ForeignKey(
        ClubGroup, on_delete=models.CASCADE, related_name="requests")
    created_at = models.DateTimeField(auto_now_add=True, auto_created=False)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="PENDING")


class ClubhouseMember(models.Model):
    SUBSCRIPTION_CHOICES = (
        ('FREE', 'Free'),
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    club = models.ForeignKey(ClubGroup, on_delete=models.CASCADE)
    subscription_type = models.CharField(
        max_length=10, choices=SUBSCRIPTION_CHOICES)
    subscription_expiration_date = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# how to check this for a particular club and also check it its pass a week since then subscription ends then turn activative to in active

# expiring_today = ClubhouseMember.objects.filter(subscription_expiration_date=today)
