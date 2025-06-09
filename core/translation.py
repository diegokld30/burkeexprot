from modeltranslation.translator import register, TranslationOptions
from .models import Categoria, Producto, EntradaBlog

@register(Categoria)
class CategoriaTO(TranslationOptions):
    fields = ('nombre',)

@register(Producto)
class ProductoTO(TranslationOptions):
    fields = ('nombre', 'descripcion',)

@register(EntradaBlog)
class EntradaBlogTO(TranslationOptions):
    fields = ('titulo', 'contenido',)
