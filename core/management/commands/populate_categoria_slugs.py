# core/management/commands/populate_categoria_slugs.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Categoria

class Command(BaseCommand):
    help = "Genera slug únicos para todas las categorías existentes"

    def handle(self, *args, **kwargs):
        for cat in Categoria.objects.all():
            base = slugify(cat.nombre_es or cat.nombre)
            # si ya existe, añade un sufijo incremental
            slug = base
            i = 1
            while Categoria.objects.filter(slug=slug).exclude(pk=cat.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            cat.slug = slug
            cat.save(update_fields=["slug"])
            self.stdout.write(self.style.SUCCESS(f"{cat.nombre} → {slug}"))
