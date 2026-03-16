from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('tree/', views.CategoryTreeView.as_view(), name='category-tree'),
]
