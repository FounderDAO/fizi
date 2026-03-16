from rest_framework import serializers
from .models import Listing, ListingPhoto, Favorite
from users.serializers import UserSerializer
from categories.serializers import CategoryFlatSerializer


class ListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingPhoto
        fields = ['id', 'image', 'order']


class ListingSerializer(serializers.ModelSerializer):
    photos = ListingPhotoSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    category = CategoryFlatSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='category', queryset=__import__('categories.models', fromlist=['Category']).Category.objects.all()
    )
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'currency',
            'category', 'category_id', 'user',
            'city', 'district', 'condition', 'status',
            'views', 'is_promoted', 'promoted_until',
            'photos', 'is_favorited', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'views', 'is_promoted', 'promoted_until',
                            'created_at', 'updated_at']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, listing=obj).exists()
        return False


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'price', 'currency',
            'category', 'city', 'district', 'condition',
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'listing', 'created_at']
