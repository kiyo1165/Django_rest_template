from django.urls import path, include
from api_user import views
from rest_framework.routers import DefaultRouter

app_name = "user"

router = DefaultRouter()
router.register('profile', views.ProfileViewSet,)

# ModelViewSetを使用した場合はrouteに紐付ける。
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name="create"),
    path('myself/', views.ManageUserView.as_view(), name="myself"),
    path('', include(router.urls))
]