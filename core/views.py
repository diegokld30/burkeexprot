from django.shortcuts import render, get_object_or_404
from .models import Categoria, EntradaBlog

def index(request):
    ultima = EntradaBlog.objects.order_by("-fecha").first()
    return render(request, "core/index.html", {"ultima": ultima})

def productos(request):
    cats = {c.slug: c for c in Categoria.objects.prefetch_related("productos")}

    return render(
        request,
        "core/productos.html",
        {
            "madera": cats.get("madera").productos.all() if "madera" in cats else [],
            "cafe":   cats.get("cafe").productos.all()   if "cafe"   in cats else [],
            "otros":  cats.get("otros").productos.all()  if "otros"  in cats else [],
        },
    )

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
