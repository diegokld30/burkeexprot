from django.contrib import admin
from .models import Categoria, Producto, EntradaBlog
from modeltranslation.admin import TranslationAdmin

@admin.register(Categoria)
class CategoriaAdmin(TranslationAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}  # rellena automáticamente al crear

@admin.register(Producto)
class ProductoAdmin(TranslationAdmin):
    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)

@admin.register(EntradaBlog)
class EntradaBlogAdmin(TranslationAdmin):
    list_display = ('titulo', 'fecha')
    date_hierarchy = 'fecha'
