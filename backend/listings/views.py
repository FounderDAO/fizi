from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q
from .models import Listing, Favorite
from .serializers import ListingListSerializer, ListingDetailSerializer


class ListingListView(generics.ListAPIView):
    serializer_class = ListingListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Listing.objects.filter(status='active').select_related('user', 'category').prefetch_related('photos')

        # Filters
        category = self.request.query_params.get('category')
        city = self.request.query_params.get('city')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        condition = self.request.query_params.get('condition')
        q = self.request.query_params.get('q')

        if category:
            qs = qs.filter(Q(category__slug=category) | Q(category__parent__slug=category))
        if city:
            qs = qs.filter(city__icontains=city)
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)
        if condition:
            qs = qs.filter(condition=condition)
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(city__icontains=q)
            )

        return qs.order_by('-is_promoted', '-created_at')


class ListingCreateView(generics.CreateAPIView):
    serializer_class = ListingDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()

    def get_serializer_class(self):
        return ListingDetailSerializer

    def get_object(self):
        obj = super().get_object()
        # Increment views on GET
        if self.request.method == 'GET':
            Listing.objects.filter(pk=obj.pk).update(views=obj.views + 1)
        return obj

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class MyListingsView(generics.ListAPIView):
    serializer_class = ListingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Listing.objects.filter(user=self.request.user).order_by('-created_at')


class FavoriteToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        listing = Listing.objects.get(pk=pk)
        fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
        if not created:
            fav.delete()
            return Response({'favorited': False})
        return Response({'favorited': True})


class FavoriteListView(generics.ListAPIView):
    serializer_class = ListingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Listing.objects.filter(
            favorited_by__user=self.request.user
        ).order_by('-favorited_by__created_at')
