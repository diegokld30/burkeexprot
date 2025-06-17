from django.shortcuts import render, get_object_or_404
from .models import Categoria, EntradaBlog

def index(request):
    ultima = EntradaBlog.objects.order_by("-fecha").first()
    return render(request, "core/index.html", {"ultima": ultima})

def productos(request):
    cats = {c.slug: c for c in Categoria.objects.prefetch_related("productos")}

    # Colores Tailwind para cada categoría
    color_map = {
        "madera": "teal",
        "cafe":   "amber",
        "cacao":  "orange",
        "otros":  "cyan",
    }

    ordered_slugs = ["madera", "cafe", "cacao", "otros"]

    categories = [
        {
            "slug": slug,
            "items": cats.get(slug).productos.all() if slug in cats else [],
            "color": color_map[slug],
            "label": slug.capitalize() if slug != "cafe" else "Café",
        }
        for slug in ordered_slugs
    ]

    return render(request, "core/productos.html", {"categories": categories})

def nosotros(request):
    return render(request, "core/nosotros.html")

def contacto(request):
    return render(request, "core/contacto.html")

def blog_lista(request):
    posts = EntradaBlog.objects.order_by("-fecha")
    return render(request, "core/blog_lista.html", {"posts": posts})

def blog_detalle(request, pk):
    post = get_object_or_404(EntradaBlog, pk=pk)
    return render(request, "core/blog_detalle.html", {"post": post})
