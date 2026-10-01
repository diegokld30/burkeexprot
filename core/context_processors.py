from django.conf import settings
from django.templatetags.static import static
from django.urls import translate_url

WHATSAPP = "573118136992"
EMAIL = "info@burkeexport.com"


def seo(request):
    """URL canónica, alternativas por idioma (hreflang) y datos de la organización."""
    base = f"{request.scheme}://{request.get_host()}"
    current = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
    alternates = []
    for code, name in settings.LANGUAGES:
        path = translate_url(request.path, code)
        alternates.append({"lang": code, "name": name, "path": path,
                           "url": base + path, "active": code == current})
    x_default = next(a["url"] for a in alternates if a["lang"] == settings.LANGUAGE_CODE)

    organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Burke Export S.A.S.",
        "alternateName": "Burke Export",
        "url": base + "/",
        "logo": base + static("icons/icon-512.png"),
        "email": EMAIL,
        "telephone": "+57 311 813 6992",
        "address": {"@type": "PostalAddress", "addressCountry": "CO"},
        "contactPoint": [{
            "@type": "ContactPoint",
            "contactType": "sales",
            "telephone": "+57 311 813 6992",
            "email": EMAIL,
            "availableLanguage": ["Spanish", "English"],
        }],
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Burke Export",
        "url": base + "/",
        "inLanguage": ["es", "en"],
    }
    return {
        "seo": {
            "base": base,
            "canonical": base + request.path,
            "alternates": alternates,
            "x_default": x_default,
            "og_locale": "en_US" if current == "en" else "es_CO",
            "og_locale_alt": "es_CO" if current == "en" else "en_US",
            "default_image": base + static("img/og-image.jpg"),
            "organization": organization,
            "website": website,
        },
        "contact": {"whatsapp": WHATSAPP, "email": EMAIL, "phone_display": "+57 311 813 6992"},
    }
