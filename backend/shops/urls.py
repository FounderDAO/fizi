from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopListView.as_view(), name='shop-list'),
    path('create/', views.ShopCreateView.as_view(), name='shop-create'),
    path('my/', views.MyShopView.as_view(), name='my-shop'),
    path('plans/', views.SubscriptionPlanListView.as_view(), name='plan-list'),
    path('<slug:slug>/', views.ShopDetailView.as_view(), name='shop-detail'),
]
