# core/management/commands/crear_editor.py
import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand

GRUPO = "Editores de contenido"
# Sin caracteres que se confunden al dictarlos (0/O, 1/l/I)
ALFABETO = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generar_password():
    return "-".join("".join(secrets.choice(ALFABETO) for _ in range(4)) for _ in range(4))


class Command(BaseCommand):
    help = ("Crea (o reinicia la contraseña de) un usuario del admin que solo puede "
            "gestionar productos, categorías y blog. Muestra la contraseña una sola vez.")

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--email", default="")

    def handle(self, *args, username, email, **options):
        grupo, _ = Group.objects.get_or_create(name=GRUPO)
        grupo.permissions.set(Permission.objects.filter(content_type__app_label="core"))

        User = get_user_model()
        user, creado = User.objects.get_or_create(username=username)
        password = generar_password()
        validate_password(password, user)

        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = False
        user.is_active = True
        user.set_password(password)
        user.save()
        user.groups.add(grupo)

        accion = "creado" if creado else "actualizado (contraseña reiniciada)"
        self.stdout.write(self.style.SUCCESS(f"Usuario editor {accion}."))
        self.stdout.write(f"  Usuario:    {username}")
        self.stdout.write(f"  Contraseña: {password}")
        self.stdout.write("Guárdala ahora: no se vuelve a mostrar.")
