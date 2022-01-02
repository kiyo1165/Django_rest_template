from rest_framework.permissions import IsAuthenticated
from core.models import Message
from api_dm import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from rest_framework import generics
# Create your views here.


class MessageViewSets(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    #自分の送信一覧
    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

    #メッセージの作成
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


#自分宛のメッセージ一覧
class InboxListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)