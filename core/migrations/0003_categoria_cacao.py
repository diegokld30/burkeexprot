from django.db import migrations


def crear_cacao(apps, schema_editor):
    Categoria = apps.get_model("core", "Categoria")
    Categoria.objects.get_or_create(
        slug="cacao",
        defaults={"nombre": "cacao", "nombre_es": "cacao", "nombre_en": "cocoa"},
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_categoria_slug'),
    ]

    operations = [
        migrations.RunPython(crear_cacao, migrations.RunPython.noop),
    ]
