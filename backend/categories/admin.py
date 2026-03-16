from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'slug', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'parent']
    prepopulated_fields = {'slug': ('name_ru',)}
    ordering = ['order']
