from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FollowRelationship


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'nickname', 'school', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('nickname', 'avatar', 'bio', 'school', 'grade', 'phone', 'is_verified')}),
    )


@admin.register(FollowRelationship)
class FollowRelationshipAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
