from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, StartConversationSerializer
from listings.models import Listing


class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            buyer=user
        ) | Conversation.objects.filter(seller=user)


class StartConversationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = StartConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        listing = generics.get_object_or_404(Listing, pk=serializer.validated_data['listing_id'])
        buyer = request.user
        seller = listing.user

        if buyer == seller:
            return Response({'error': 'Cannot message yourself'}, status=status.HTTP_400_BAD_REQUEST)

        conv, _ = Conversation.objects.get_or_create(
            listing=listing, buyer=buyer,
            defaults={'seller': seller}
        )

        Message.objects.create(
            conversation=conv,
            sender=buyer,
            text=serializer.validated_data['message']
        )

        return Response(ConversationSerializer(conv, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conv = generics.get_object_or_404(
            Conversation, pk=self.kwargs['conv_id'],
            **{'buyer': self.request.user} if hasattr(self.request.user, 'pk') else {}
        )
        # Mark messages as read
        conv.messages.exclude(sender=self.request.user).update(is_read=True)
        return conv.messages.all()

    def perform_create(self, serializer):
        conv = generics.get_object_or_404(Conversation, pk=self.kwargs['conv_id'])
        serializer.save(sender=self.request.user, conversation=conv)
