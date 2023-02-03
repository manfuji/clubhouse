from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(MemberVote)
class MemberVoteAdmin(admin.ModelAdmin):
    list_display_list = ("vote_product_id",)
    list_display = ("vote_count", "vote_product_id")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display_list = ("name",)
    list_display = ("name", "price", "created_at")


@admin.register(ClubGroup)
class ClubAdmin(admin.ModelAdmin):
    list_display_list = ("name",)
    list_display = ("is_active", "name")
