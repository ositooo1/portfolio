document.addEventListener("click", (evento) => {
  // Mensaje de prueba: muestra qué elemento recibió el clic (borralo cuando ande)

  // ---- Subir foto, banner o CV ----
  const subir = evento.target.closest("[data-subir]");
  if (subir) {
    const modal = document.getElementById("modal-subida");
    const formulario = modal.querySelector("form");
    formulario.reset();

    // La ruta, el título y los formatos vienen en el botón
    formulario.action = subir.dataset.subir;
    formulario.querySelector("[name=archivo]").accept = subir.dataset.accept;
    modal.querySelector(".modal-titulo").textContent = subir.dataset.titulo;
    modal.querySelector(".ayuda").textContent = subir.dataset.ayuda;

    modal.showModal();
    return;
  }

  // ---- Abrir el modal de edición de una sección ----
  // El botón trae los datos actuales en atributos data-*,
  // y se copian a los campos que tienen el mismo nombre.
  const boton = evento.target.closest("[data-abrir]");
  if (boton) {
    const modal = document.getElementById("modal-" + boton.dataset.abrir);
    const formulario = modal.querySelector("form");
    formulario.reset();

    const id = boton.dataset.id || "";
    formulario.querySelector("[name=id]").value = id;

    // Con id se edita un elemento existente; sin id se agrega uno nuevo
    const nombre = modal.dataset.nombre;
    const titulo = modal.querySelector(".modal-titulo");
    titulo.textContent =
      nombre === "Perfil"
        ? "Editar perfil"
        : (id ? "Editar " : "Agregar ") + nombre;

    formulario
      .querySelectorAll("input[name], textarea[name], select[name]")
      .forEach((campo) => {
        if (campo.name === "id" || campo.name === "csrf_token") return;
        if (boton.dataset[campo.name] !== undefined) {
          campo.value = boton.dataset[campo.name];
        }
      });

    modal.showModal();
    return;
  }

  // ---- Cerrar con el botón Cancelar ----
  if (evento.target.closest("[data-cerrar]")) {
    evento.target.closest("dialog").close();
    return;
  }

  // ---- Cerrar al hacer clic fuera de la ventana ----
  if (evento.target.tagName === "DIALOG") {
    evento.target.close();
  }
});
