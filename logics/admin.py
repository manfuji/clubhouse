from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(MemberVote)
class MemberVoteAdmin(admin.ModelAdmin):
    list_display_links = ("vote_product",)
    list_display = ("voter", "vote_product")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display_links = ["name",]
    list_display = ["name", "price", "created_at"]
    list_filter = ["active", "is_completed"]
    search_fields = ["name"]


@admin.register(ClubGroup)
class ClubAdmin(admin.ModelAdmin):
    list_display_links = ["name",]
    list_display = ["is_active", "name"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(ClubhouseMember)
class ClubmemberAdmin(admin.ModelAdmin):
    list_display_list = ["user",]
    list_display = ["active", "user", "subscription_type"]
    list_filter = ["active", "subscription_type"]
    search_fields = ["user__first_name", " user__last_name"]


@admin.register(RequestToJoinGroup)
class RequestToJoinGroup(admin.ModelAdmin):
    list_display_list = ["user",]
    list_display = ["status", "user", "club_group"]
    list_filter = ["status", "club_group"]
    search_fields = ["user__first_name", " user__last_name"]


@admin.register(ProductCategory)
class RequestToJoinGroup(admin.ModelAdmin):
    list_display_list = ["name",]
    list_display = ["name",]
    list_filter = ["name", ]
    search_fields = ["name"]
