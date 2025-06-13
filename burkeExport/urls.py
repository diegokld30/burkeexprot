from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Necesario para {% url 'set_language' %}
    path('i18n/', include('django.conf.urls.i18n')),

    # Panel de administración
    path('admin/', admin.site.urls),

    # Tu aplicación principal
    path('', include('core.urls')),
]

# Sirve MEDIA en DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
