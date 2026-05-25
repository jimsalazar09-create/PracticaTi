document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".btn-toggle").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      const res = await fetch(`/toggle/${id}`, { method: "POST" });
      const data = await res.json();

      // Actualizar el texto del estado en la tarjeta
      const card = btn.closest(".card");
      card.querySelector(".estado").textContent = data.nuevo_estado;

      // Actualizar el color del borde
      card.classList.remove("pendiente", "en-progreso", "completada");
      card.classList.add(data.nuevo_estado.replace(" ", "-"));
    });
  });
});