from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from .models import Categoria, EntradaBlog, Producto


@override_settings(SECURE_SSL_REDIRECT=False)
class PaginasPublicasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        madera = Categoria.objects.get_or_create(slug="madera", defaults={"nombre": "madera"})[0]
        Producto.objects.create(nombre="Decks", descripcion="d", imagen="productos/Decks.jpg", categoria=madera)
        cls.post = EntradaBlog.objects.create(
            titulo_es="Madera Teca", titulo_en="Teca wood",
            contenido="<script>alert(1)</script>\n\nSegundo párrafo", imagen="blog/teca.jpg"
        )

    def test_paginas_responden_en_ambos_idiomas(self):
        urls = ["index", "productos", "nosotros", "contacto", "blog_lista"]
        for lang in ["es", "en"]:
            with translation.override(lang):
                for name in urls:
                    with self.subTest(lang=lang, url=name):
                        r = self.client.get(reverse(name))
                        self.assertEqual(r.status_code, 200)
                        self.assertContains(r, f'<html lang="{lang}"')
                r = self.client.get(self.post.get_absolute_url())
                self.assertEqual(r.status_code, 200)

    def test_urls_en_ingles_traducidas(self):
        with translation.override("en"):
            self.assertEqual(reverse("productos"), "/en/products/")
            self.assertEqual(reverse("nosotros"), "/en/about-us/")
        self.assertEqual(reverse("productos"), "/productos/")
        r = self.client.get("/en/products/")
        self.assertContains(r, "Discover Our Collection")

    def test_seo_head(self):
        r = self.client.get("/productos/")
        self.assertContains(r, '<link rel="canonical" href="http://testserver/productos/">')
        self.assertContains(r, 'hreflang="en" href="http://testserver/en/products/"')
        self.assertContains(r, 'hreflang="x-default" href="http://testserver/productos/"')
        self.assertContains(r, '<meta name="description" content="')
        self.assertContains(r, 'property="og:image"')
        self.assertContains(r, '"@type": "Organization"')

    def test_blog_url_legible_y_redireccion(self):
        self.assertEqual(self.post.get_absolute_url(), f"/blog/{self.post.pk}/madera-teca/")
        r = self.client.get(f"/blog/{self.post.pk}/")
        self.assertRedirects(r, self.post.get_absolute_url(), status_code=301)
        r = self.client.get(self.post.get_absolute_url())
        self.assertContains(r, '"@type": "BlogPosting"')
        self.assertContains(r, f'hreflang="en" href="http://testserver/en/blog/{self.post.pk}/teca-wood/"')

    def test_blog_no_ejecuta_html(self):
        r = self.client.get(self.post.get_absolute_url())
        self.assertNotContains(r, "<script>alert(1)</script>")
        self.assertContains(r, "&lt;script&gt;")

    def test_blog_inexistente_da_404(self):
        r = self.client.get("/blog/999/x/")
        self.assertEqual(r.status_code, 404)
        self.assertContains(r, "noindex", status_code=404)

    def test_categoria_cacao_existe(self):
        self.assertTrue(Categoria.objects.filter(slug="cacao").exists())

    def test_cabeceras_de_seguridad(self):
        r = self.client.get(reverse("index"))
        self.assertIn("script-src 'self'", r["Content-Security-Policy"])
        self.assertEqual(r["X-Frame-Options"], "DENY")
        self.assertIn("Permissions-Policy", r)

    def test_sin_herramientas_de_desarrollo_ni_cdn(self):
        r = self.client.get(reverse("index"))
        self.assertNotContains(r, "brandPicker")
        self.assertNotContains(r, "cdn.jsdelivr.net")

    def test_robots_y_sitemap(self):
        r = self.client.get("/robots.txt")
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "admin")
        self.assertContains(r, "Sitemap: http://testserver/sitemap.xml")
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "/en/products/")
        self.assertContains(r, f"/blog/{self.post.pk}/madera-teca/")
        self.assertContains(r, 'hreflang="x-default"')

    def test_manifest(self):
        r = self.client.get("/site.webmanifest")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["name"], "Burke Export")


@override_settings(SECURE_SSL_REDIRECT=False, AXES_FAILURE_LIMIT=3)
class FuerzaBrutaTests(TestCase):
    def test_bloquea_tras_intentos_fallidos(self):
        from django.conf import settings
        url = "/" + settings.ADMIN_URL + "login/"
        for _ in range(3):
            self.client.post(url, {"username": "x", "password": "mal"}, REMOTE_ADDR="10.0.0.9")
        r = self.client.post(url, {"username": "x", "password": "mal"}, REMOTE_ADDR="10.0.0.9")
        self.assertEqual(r.status_code, 429)


class CrearEditorTests(TestCase):
    def test_crea_editor_con_permisos_limitados(self):
        from io import StringIO
        from django.contrib.auth import get_user_model
        from django.core.management import call_command
        out = StringIO()
        call_command("crear_editor", "cliente", "--email", "c@example.com", stdout=out)
        password = out.getvalue().split("Contraseña: ")[1].split()[0]
        user = get_user_model().objects.get(username="cliente")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.has_perm("core.add_producto"))
        self.assertTrue(user.has_perm("core.change_entradablog"))
        self.assertFalse(user.has_perm("auth.add_user"))
