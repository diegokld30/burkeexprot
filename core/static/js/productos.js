// Pestañas de categorías. Respeta el ancla (#panel-cafe…) que llega desde la portada o el pie.
const tabs = document.querySelectorAll(".tab-btn");
const panels = document.querySelectorAll('[role="tabpanel"]');

function activate(target) {
  tabs.forEach((t) => t.setAttribute("aria-selected", String(t.dataset.tab === target)));
  panels.forEach((p) => p.classList.toggle("hidden", p.id !== `panel-${target}`));
}

tabs.forEach((tab) =>
  tab.addEventListener("click", () => {
    activate(tab.dataset.tab);
    history.replaceState(null, "", `#panel-${tab.dataset.tab}`);
  })
);

function fromHash() {
  const slug = location.hash.replace("#panel-", "");
  if (slug && document.getElementById(`panel-${slug}`)) {
    activate(slug);
    document.querySelector('[role="tablist"]').scrollIntoView({ block: "start" });
  }
}
window.addEventListener("hashchange", fromHash);
fromHash();
