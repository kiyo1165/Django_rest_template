from rest_framework import permissions


# SAFE_METHODSは安全なgetメソッドが格納されている。
# ログインしているユーザー以外はfalseを返す
class ProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.id == request.user.id

