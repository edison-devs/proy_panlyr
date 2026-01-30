// home.js
// 🧠 Script para manejar los efectos de estilos en Home

document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       CARRITO SIDEBAR
    ========================== */

    const cartButton = document.getElementById("cart-button");
    const cartSidebar = document.getElementById("cart-sidebar");
    const closeCartBtn = document.getElementById("close-cart");
    const overlay = document.getElementById("cart-overlay");

    function showCartSidebar() {
        if (cartSidebar && overlay) {
            cartSidebar.classList.add("show");
            overlay.classList.add("show");
        }
    }

    function hideCartSidebar() {
        if (cartSidebar && overlay) {
            cartSidebar.classList.remove("show");
            overlay.classList.remove("show");
        }
    }

    if (cartButton) {
        cartButton.addEventListener("click", showCartSidebar);
    }

    if (closeCartBtn) {
        closeCartBtn.addEventListener("click", hideCartSidebar);
    }

    if (overlay) {
        overlay.addEventListener("click", hideCartSidebar);
    }

    /* =========================
       RESEÑAS (MODAL)
    ========================== */

    const reviewModalEl = document.getElementById("review-modal");
    const submitReviewBtn = document.getElementById("submit-review");

    if (submitReviewBtn && reviewModalEl) {
        submitReviewBtn.addEventListener("click", function () {
            alert("¡Gracias por tu reseña! 💛");
            const modal = bootstrap.Modal.getInstance(reviewModalEl);
            if (modal) modal.hide();
        });
    }

    /* =========================
       FORMULARIO DE CONTACTO
       (si existe)
    ========================== */

    const contactForm = document.getElementById("contact-form");

    if (contactForm) {
        contactForm.addEventListener("submit", function (e) {
            e.preventDefault();
            alert("Mensaje enviado correctamente 📩");
            contactForm.reset();
        });
    }

    /* =========================
       FORMULARIO DE PEDIDO
       (si existe)
    ========================== */

    const orderForm = document.getElementById("order-form");
    const orderModalEl = document.getElementById("order-confirmation-modal");

    if (orderForm && orderModalEl) {
        orderForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const orderNumber = Math.floor(Math.random() * 100000);
            const orderNumberEl = document.getElementById("order-number");

            if (orderNumberEl) {
                orderNumberEl.textContent = orderNumber;
            }

            const modal = new bootstrap.Modal(orderModalEl);
            modal.show();

            orderForm.reset();
            hideCartSidebar();
        });
    }

});