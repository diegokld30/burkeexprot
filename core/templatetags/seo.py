import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_ESCAPES = {ord("<"): "\\u003C", ord(">"): "\\u003E", ord("&"): "\\u0026"}


@register.filter
def jsonld(value):
    """Serializa datos estructurados para <script type="application/ld+json"> de forma segura."""
    return mark_safe(json.dumps(value, ensure_ascii=False).translate(_ESCAPES))
