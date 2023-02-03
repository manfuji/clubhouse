from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(AccountUser)
class ClubAdmin(admin.ModelAdmin):
    list_display_list = ("name",)
    list_display = ("name", "is_active")
