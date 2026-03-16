from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_uz', 'name_en', 'slug', 'parent',
                  'icon', 'order', 'is_active', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []


class CategoryFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_uz', 'name_en', 'slug', 'parent',
                  'icon', 'order', 'is_active']
