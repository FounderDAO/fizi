from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    listing_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_uz', 'name_en', 'slug', 'icon', 'parent', 'listing_count', 'children']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data

    def get_listing_count(self, obj):
        return obj.listings.filter(status='active').count()


class CategoryFlatSerializer(serializers.ModelSerializer):
    listing_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_uz', 'name_en', 'slug', 'icon', 'parent', 'listing_count']

    def get_listing_count(self, obj):
        return obj.listings.filter(status='active').count()
