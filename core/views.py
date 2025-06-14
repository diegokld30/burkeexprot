from django.shortcuts import render, get_object_or_404
from .models import Categoria, EntradaBlog

def index(request):
    ultima = EntradaBlog.objects.order_by("-fecha").first()
    return render(request, "core/index.html", {"ultima": ultima})

def productos(request):
    # Consigue las categorías con sus productos
    cats = {c.slug: c for c in Categoria.objects.prefetch_related("productos")}

    # Prepara la lista para el template
    categories = [
        {
            "slug": "madera",
            "items": cats.get("madera").productos.all() if "madera" in cats else [],
            "color": "teal",
            "label": "Madera",
        },
        {
            "slug": "cafe",
            "items": cats.get("cafe").productos.all() if "cafe" in cats else [],
            "color": "amber",
            "label": "Café",
        },
        {
            "slug": "otros",
            "items": cats.get("otros").productos.all() if "otros" in cats else [],
            "color": "cyan",
            "label": "Otros",
        },
    ]

    return render(request, "core/productos.html", {
        "categories": categories
    })

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
