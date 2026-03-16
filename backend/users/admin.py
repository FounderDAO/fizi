from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPCode, Review


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone', 'name', 'is_verified', 'rating', 'created_at']
    list_filter = ['is_verified', 'is_staff', 'is_active']
    search_fields = ['phone', 'name']
    ordering = ['-created_at']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Info', {'fields': ('name', 'avatar', 'bio', 'city')}),
        ('Status', {'fields': ('is_verified', 'rating', 'review_count')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'password1', 'password2'),
        }),
    )


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ['phone', 'code', 'is_used', 'created_at']
    list_filter = ['is_used']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'target', 'rating', 'created_at']
