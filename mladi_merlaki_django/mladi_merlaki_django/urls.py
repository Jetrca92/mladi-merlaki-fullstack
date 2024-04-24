from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

api_v1_patterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('portfolio/', include('portfolio.urls')),
    path('marketdata/', include('marketdata.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
