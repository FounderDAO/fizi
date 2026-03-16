from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Listing, ListingPhoto, Favorite
from categories.serializers import CategoryFlatSerializer

# ---------------------------------------------------------------------------
# Backward-compat alias used by chat app
# ---------------------------------------------------------------------------

User = get_user_model()


class ListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingPhoto
        fields = ['id', 'image', 'order']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'avatar', 'phone', 'is_verified', 'rating']


class ListingListSerializer(serializers.ModelSerializer):
    """Compact serializer for listing cards."""
    cover_photo = serializers.SerializerMethodField()
    author = AuthorSerializer(source='user', read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = ['id', 'title', 'price', 'currency', 'city', 'condition',
                  'cover_photo', 'author', 'is_favorite', 'views', 'created_at', 'is_promoted']

    def get_cover_photo(self, obj):
        photo = obj.photos.first()
        if photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(photo.image.url)
        return None

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False


class ListingDetailSerializer(serializers.ModelSerializer):
    """Full serializer for listing detail page."""
    photos = ListingPhotoSerializer(many=True, read_only=True)
    author = AuthorSerializer(source='user', read_only=True)
    category = CategoryFlatSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    is_favorite = serializers.SerializerMethodField()
    uploaded_photos = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'price', 'currency', 'city', 'district',
                  'condition', 'status', 'category', 'category_id', 'author',
                  'photos', 'uploaded_photos', 'is_favorite', 'views', 'is_promoted',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'views', 'is_promoted', 'created_at', 'updated_at']

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False

    def create(self, validated_data):
        uploaded_photos = validated_data.pop('uploaded_photos', [])
        category_id = validated_data.pop('category_id', None)
        listing = Listing.objects.create(
            user=self.context['request'].user,
            category_id=category_id,
            **validated_data
        )
        for i, photo in enumerate(uploaded_photos):
            ListingPhoto.objects.create(listing=listing, image=photo, order=i)
        return listing

# Backward-compat alias for chat app
ListingSerializer = ListingDetailSerializer
