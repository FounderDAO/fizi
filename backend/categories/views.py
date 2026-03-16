from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer, CategoryFlatSerializer


class CategoryListView(generics.ListAPIView):
    """Returns root categories with nested children."""
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.filter(parent=None, is_active=True)


class CategoryDetailView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(is_active=True)
    lookup_field = 'slug'
