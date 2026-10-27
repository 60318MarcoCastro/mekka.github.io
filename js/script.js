/* =========================================================
   MEKKA - Taller Mecánico
   Modo oscuro y avisos de botones pendientes
   ========================================================= */

// Aplica el tema guardado lo antes posible para evitar parpadeo
(function () {
  try {
    if (localStorage.getItem("mekka-theme") === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  } catch (e) {
    // localStorage no disponible: se usa el tema claro
  }
})();

document.addEventListener("DOMContentLoaded", function () {
  // ---------- Botón de modo oscuro ----------
  var toggle = document.getElementById("theme-toggle");

  function updateToggle() {
    if (!toggle) return;
    var isDark = document.documentElement.getAttribute("data-theme") === "dark";
    toggle.querySelector(".icon").textContent = isDark ? "☀️" : "🌙";
    toggle.querySelector(".label").textContent = isDark ? "Modo claro" : "Modo oscuro";
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var isDark = document.documentElement.getAttribute("data-theme") === "dark";
      if (isDark) {
        document.documentElement.removeAttribute("data-theme");
      } else {
        document.documentElement.setAttribute("data-theme", "dark");
      }
      try {
        localStorage.setItem("mekka-theme", isDark ? "light" : "dark");
      } catch (e) {}
      updateToggle();
    });
    updateToggle();
  }

  // ---------- Inicio de sesión (por ahora solo redirige) ----------
  var loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
      event.preventDefault();
      window.location.href = "menu.html";
    });
  }

  // ---------- Botones aún sin funcionalidad ----------
  var toast = document.getElementById("toast");
  var timer;
  document.querySelectorAll("[data-pending]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!toast) return;
      toast.textContent = "\"" + btn.dataset.pending + "\" estará disponible próximamente";
      toast.classList.add("show");
      clearTimeout(timer);
      timer = setTimeout(function () {
        toast.classList.remove("show");
      }, 2200);
    });
  });
});
