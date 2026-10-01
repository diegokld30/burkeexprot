from django.shortcuts import render, get_object_or_404, redirect
from django.utils import translation
from django.utils.text import Truncator
from django.utils.translation import gettext as _

from .models import Categoria, EntradaBlog

SITE = "Burke Export"


def _titulo(texto):
    return f"{texto} | {SITE}"


def index(request):
    ultima = EntradaBlog.objects.order_by("-fecha").first()
    return render(request, "core/index.html", {
        "ultima": ultima,
        "page_title": _("Burke Export | Exportadores de madera, café y cacao de Colombia"),
        "page_description": _(
            "Empresa colombo-española exportadora de derivados de maderas cultivadas, "
            "café y cacao de Colombia. Procedencia legal, trazabilidad y logística global."
        ),
    })


def productos(request):
    cats = {c.slug: c for c in Categoria.objects.prefetch_related("productos")}
    labels = {"madera": "Madera", "cafe": "Café", "cacao": "Cacao", "otros": "Otros"}

    categories = [
        {
            "slug": slug,
            "items": cats[slug].productos.all() if slug in cats else [],
            "label": label,
        }
        for slug, label in labels.items()
    ]

    return render(request, "core/productos.html", {
        "categories": categories,
        "page_title": _titulo(_("Productos: madera, café y cacao de exportación")),
        "page_description": _(
            "Decks, madera estructural, pisos interiores y módulos prefabricados en maderas "
            "cultivadas, además de café y cacao colombianos con calidad de exportación."
        ),
    })


def nosotros(request):
    return render(request, "core/nosotros.html", {
        "page_title": _titulo(_("Nosotros")),
        "page_description": _(
            "Conoce a Burke Export: un equipo multicultural que lleva la esencia de Colombia "
            "al mundo con calidad, integridad y sostenibilidad."
        ),
    })


def contacto(request):
    return render(request, "core/contacto.html", {
        "page_title": _titulo(_("Contacto")),
        "page_description": _(
            "Habla con un asesor de Burke Export y recibe una propuesta personalizada "
            "para tu proyecto de importación."
        ),
    })


def blog_lista(request):
    posts = EntradaBlog.objects.order_by("-fecha")
    return render(request, "core/blog_lista.html", {
        "posts": posts,
        "page_title": _titulo(_("Blog y noticias")),
        "page_description": _(
            "Noticias, proyectos y conocimiento sobre maderas cultivadas, café y cacao "
            "de Colombia para el mercado internacional."
        ),
    })


def blog_detalle(request, pk, slug=None):
    post = get_object_or_404(EntradaBlog, pk=pk)
    canonical_path = post.get_absolute_url()
    if request.path != canonical_path:
        return redirect(canonical_path, permanent=True)

    base = f"{request.scheme}://{request.get_host()}"
    image = base + post.imagen.url if post.imagen else None
    description = Truncator(post.contenido).words(30, truncate="…")

    alternates = []
    for code, name in [("es", "Español"), ("en", "English")]:
        with translation.override(code):
            path = post.get_absolute_url()
        alternates.append({"lang": code, "name": name, "path": path, "url": base + path,
                           "active": code == request.LANGUAGE_CODE})

    article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.titulo,
        "description": description,
        "datePublished": post.fecha.isoformat(),
        "inLanguage": request.LANGUAGE_CODE,
        "mainEntityOfPage": base + canonical_path,
        "author": {"@type": "Organization", "name": "Burke Export S.A.S."},
        "publisher": {"@type": "Organization", "name": "Burke Export S.A.S."},
    }
    if image:
        article["image"] = [image]

    return render(request, "core/blog_detalle.html", {
        "post": post,
        "page_title": _titulo(post.titulo),
        "page_description": description,
        "og_type": "article",
        "og_image": image,
        "hreflang_alternates": alternates,
        "article_ld": article,
    })
