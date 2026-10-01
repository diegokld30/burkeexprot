// Marca que hay JS (activa las animaciones de aparición sin ocultar contenido a quien no lo tenga)
document.documentElement.classList.add("js");

// Sombra suave en la cabecera al hacer scroll
const header = document.getElementById("site-header");
const onScroll = () => header && header.classList.toggle("shadow-[0_8px_30px_-12px_rgba(14,37,43,0.18)]", window.scrollY > 8);
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Cierra el menú móvil al pulsar fuera o al elegir una opción
document.querySelectorAll("details[data-menu]").forEach((menu) => {
  document.addEventListener("click", (e) => { if (!menu.contains(e.target)) menu.removeAttribute("open"); });
  menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => menu.removeAttribute("open")));
});

// Aparición suave de secciones
const revealables = document.querySelectorAll("[data-reveal]");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { entry.target.classList.add("is-visible"); io.unobserve(entry.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  revealables.forEach((el) => io.observe(el));
} else {
  revealables.forEach((el) => el.classList.add("is-visible"));
}
