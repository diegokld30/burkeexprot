from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import EntradaBlog


class PaginasSitemap(Sitemap):
    protocol = "https"
    i18n = True
    alternates = True
    x_default = True
    changefreq = "monthly"

    def items(self):
        return ["index", "productos", "nosotros", "contacto", "blog_lista"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "index" else 0.8


class BlogSitemap(Sitemap):
    protocol = "https"
    i18n = True
    alternates = True
    x_default = True
    changefreq = "yearly"
    priority = 0.6

    def items(self):
        return EntradaBlog.objects.order_by("-fecha")

    def lastmod(self, obj):
        return obj.fecha


sitemaps = {"paginas": PaginasSitemap, "blog": BlogSitemap}
