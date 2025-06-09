from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,                 name='index'),
    path('productos/', views.productos,   name='productos'),
    path('nosotros/',  views.nosotros,    name='nosotros'),
    path('contacto/',  views.contacto,    name='contacto'),
    path('blog/',      views.blog_lista,  name='blog_lista'),
    path('blog/<int:pk>/', views.blog_detalle, name='blog_detalle'),
]
