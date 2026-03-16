from django.urls import path
from . import views

urlpatterns = [
    path('suggest/', views.AIListingSuggestView.as_view(), name='ai-suggest'),
]
