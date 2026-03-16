from django.contrib import admin
from .models import Listing, ListingPhoto, Favorite


class ListingPhotoInline(admin.TabularInline):
    model = ListingPhoto
    extra = 0


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'price', 'city', 'status', 'views', 'created_at']
    list_filter = ['status', 'condition', 'is_promoted', 'city']
    search_fields = ['title', 'description', 'user__phone']
    inlines = [ListingPhotoInline]
    ordering = ['-created_at']
