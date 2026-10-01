from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path('', views.index,                       name='index'),
    path(_('productos/'), views.productos,      name='productos'),
    path(_('nosotros/'),  views.nosotros,       name='nosotros'),
    path(_('contacto/'),  views.contacto,       name='contacto'),
    path('blog/',      views.blog_lista,        name='blog_lista'),
    path('blog/<int:pk>/', views.blog_detalle,  name='blog_detalle_corto'),
    path('blog/<int:pk>/<slug:slug>/', views.blog_detalle, name='blog_detalle'),
]
