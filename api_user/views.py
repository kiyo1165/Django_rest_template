from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from api_user import serializers
from core.models import Profile, User

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from core import ownpermissions

# Create your views here.


# ユーザーの作成
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


#ユーザー情報の更新
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    #認証
    authentication_classes = (authentication.TokenAuthentication, )
    # 権限：ログインユーザーのみ
    permission_classes = (permissions.IsAuthenticated,)

    #getメソッド時に自分のオブジェクトのみ返すようにする。
    def get_object(self):
        return self.request.user


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (authentication.TokenAuthentication, ownpermissions.ProfilePermission)
    permission_classes = (permissions.IsAuthenticated, )

    #登録しているユーザーのProfileのみ表示できるようにする。
    def get_queryset(self):
        #自身のprofileオブジェクトを取得、なければNone
        try:
            is_friend = Profile.objects.get(userpro=self.request.user)
        except Profile.DoesNotExist:
            is_friend = None
            return

        #友達になっているuserのフィルターを作成
        friend_filter = Q()
        for friend in is_friend.friends.all():
            friend_filter = friend_filter | Q(userpro=friend)

        return self.queryset.filter(friend_filter)

    def perform_create(self, serializer):
        try:
            serializer.save(userpro=self.request.user)
        except IntegrityError:
            # profile と userモデルはone to oneなのでIntegrityErrorが発生させる。
            raise ValidationError("User can have only one own profile")


