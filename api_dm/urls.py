from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_dm import views

router = DefaultRouter()
router.register('message', views.MessageViewSets)

app_name = "dm"


urlpatterns = [
    path('', include(router.urls)),
    path('inbox/', views.InboxListView.as_view(), name="inbox")

]