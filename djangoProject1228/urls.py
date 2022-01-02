from django.contrib import admin
from django.urls import path, include
from djangoProject1228 import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authen/', views.obtain_auth_token), #トークンの取得
    path('api/user/', include('api_user.urls')),
    path('api/dm/', include('api_dm.urls')),
    path('api/tweet/', include('api_tweet.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)