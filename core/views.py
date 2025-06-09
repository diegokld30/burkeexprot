from django.shortcuts import render, get_object_or_404
from .models import Categoria, EntradaBlog

def index(request):
    ultimas = EntradaBlog.objects.order_by('-fecha')[:3]
    return render(request, 'core/index.html', {'ultimas': ultimas})

def productos(request):
    cats = { c.nombre.lower(): c for c in
             Categoria.objects.prefetch_related('productos') }

    madera = cats.get('madera').productos.all() if 'madera' in cats else []
    cafe   = cats.get('café').productos.all()   if 'café'   in cats else []
    otros  = cats.get('otros').productos.all()  if 'otros'  in cats else []

    return render(request, 'core/productos.html', {
        'madera': madera,
        'cafe':   cafe,
        'otros':  otros,
    })

def nosotros(request):
    return render(request, 'core/nosotros.html')

def contacto(request):
    return render(request, 'core/contacto.html')

def blog_lista(request):
    posts = EntradaBlog.objects.order_by('-fecha')
    return render(request, 'core/blog_lista.html', {'posts': posts})

def blog_detalle(request, pk):
    post = get_object_or_404(EntradaBlog, pk=pk)
    return render(request, 'core/blog_detalle.html', {'post': post})
