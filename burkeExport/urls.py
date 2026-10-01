from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from core.sitemaps import sitemaps

urlpatterns = [
    # Necesario para {% url 'set_language' %}
    path('i18n/', include('django.conf.urls.i18n')),

    # Panel de administración (ruta configurable con ADMIN_URL en .env)
    path(settings.ADMIN_URL, admin.site.urls),

    # SEO
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('site.webmanifest', TemplateView.as_view(
        template_name='site.webmanifest', content_type='application/manifest+json')),
]

# Sirve MEDIA (imágenes subidas desde el admin) si nginx no lo hace
if settings.DEBUG or settings.SERVE_MEDIA:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Sitio público: español sin prefijo (/productos/) e inglés con /en/ (/en/products/)
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    prefix_default_language=False,
)
