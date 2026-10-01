// Envía el formulario de contacto a WhatsApp con el mensaje armado
const form = document.getElementById("contactForm");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const d = Object.fromEntries(new FormData(form));
  const raw = `
*Nuevo contacto BurkeExport*
👤 *Nombre:* ${d.name}
📧 *Email:* ${d.email}
📱 *Teléfono:* ${d.phone}
🏷️ *Interés:* ${d.type}
📝 *Mensaje:* ${d.message}`.trim();

  const url = `https://api.whatsapp.com/send?phone=${form.dataset.whatsapp}&text=${encodeURIComponent(raw)}`;
  window.open(url, "_blank", "noopener");
});
