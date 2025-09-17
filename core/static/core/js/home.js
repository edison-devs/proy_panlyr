// home.js
// 🧠 Script para manejar los sliders de catálogo en Home

function mostrarSlider(tipo) {
  const destacados = document.getElementById('slider-destacados');
  const recientes = document.getElementById('slider-recientes');

  if (tipo === 'destacados') {
    destacados.classList.remove('d-none');
    recientes.classList.add('d-none');
  } else {
    recientes.classList.remove('d-none');
    destacados.classList.add('d-none');
  }
}

// Opcional: desplazar suavemente al catálogo cuando se seleccione un filtro
document.addEventListener("DOMContentLoaded", () => {
  const botones = document.querySelectorAll("button[onclick^='mostrarSlider']");
  botones.forEach(boton => {
    boton.addEventListener("click", () => {
      document.querySelector("#catalogo").scrollIntoView({ behavior: "smooth" });
    });
  });
});


