from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listing-list'),
    path('create/', views.ListingCreateView.as_view(), name='listing-create'),
    path('my/', views.MyListingsView.as_view(), name='my-listings'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='listing-detail'),
    path('<int:pk>/favorite/', views.FavoriteToggleView.as_view(), name='listing-favorite'),
]
