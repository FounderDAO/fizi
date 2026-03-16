from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='conversation-list'),
    path('start/', views.StartConversationView.as_view(), name='start-conversation'),
    path('<int:conv_id>/messages/', views.MessageListView.as_view(), name='message-list'),
]
