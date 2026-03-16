from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer, CategoryFlatSerializer


class CategoryTreeView(APIView):
    """Returns full category tree (root categories with children)."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        roots = Category.objects.filter(parent=None, is_active=True).order_by('order')
        serializer = CategorySerializer(roots, many=True)
        return Response(serializer.data)


class CategoryListView(generics.ListAPIView):
    """Flat list of all categories (no pagination)."""
    queryset = Category.objects.filter(is_active=True).order_by('order')
    serializer_class = CategoryFlatSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
