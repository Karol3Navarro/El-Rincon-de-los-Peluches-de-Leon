
$(document).ready(function() {
    // Mensajes que desaparecen automáticamente
    $("#idMensajes").delay(2000).fadeOut("slow");
});

document.addEventListener("DOMContentLoaded", () => {

    const estado = document.getElementById("estado_revision");
    const campos = document.getElementById("campos_entrega");

    if (!estado || !campos) return;

    const toggle = () => {
        campos.style.display =
            estado.value === "Vendido" ? "block" : "none";
    };

    estado.addEventListener("change", toggle);
    toggle();
});

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) return; // evita errores en otras páginas

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: window.innerWidth < 768 ? 'listWeek' : 'dayGridMonth',
        locale: 'es',

        height: 'auto',

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,listWeek'
        },

        events: '/admin_peluches/eventos/',

        eventClick: function(info) {

            const fecha = new Date(info.event.start);
            const id = info.event.id;

            document.getElementById("modalTitulo").innerText = info.event.title;

            document.getElementById("modalFecha").innerText =
                "📅 " + fecha.toLocaleDateString() +
                " ⏰ " + fecha.toLocaleTimeString();

            document.getElementById("modalLugar").innerText =
                "📍 " + (info.event.extendedProps.description || "No definido");

            document.getElementById("modalImagen").src =
                info.event.extendedProps.image || "";

            const form = document.getElementById("formEntregado");
            if (form) {
                form.action = `/admin_peluches/entregado/${id}/`;
            }

            const modal = new bootstrap.Modal(document.getElementById('eventoModal'));
            modal.show();
        }
    });

    calendar.render();
});

document.addEventListener("DOMContentLoaded", function(){
    setTimeout(() => {
        const swiper = new Swiper(".mySwiperPeluche", {
            slidesPerView: 1,
            spaceBetween: 10,
            loop: true,
            autoplay: {
                delay: 3000,
                disableOnInteraction: false,
            },
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
        });
    }, 100);
});

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("imagenesInput");
    const preview = document.getElementById("preview");
    const placeholder = document.getElementById("placeholder");

    if (!input || !preview || !placeholder) return;

    let archivos = [];

    input.onchange = function () {
        archivos = Array.from(this.files);
        renderPreview();
    };

    function renderPreview() {
        preview.innerHTML = "";

        if (archivos.length > 0) {
            placeholder.style.display = "none";
        } else {
            placeholder.style.display = "block";
        }

        archivos.forEach((file, index) => {
            if (!file.type.startsWith("image/")) return;

            const reader = new FileReader();

            reader.onload = function (e) {
                const container = document.createElement("div");
                container.style.position = "relative";

                const img = document.createElement("img");
                img.src = e.target.result;

                // Botón eliminar
                const btn = document.createElement("button");
                btn.innerHTML = "X"; // mejor símbolo
                btn.classList.add("btn-eliminar");
                btn.style.position = "absolute";
                btn.style.top = "5px";
                btn.style.right = "5px";
                btn.style.background = "red";
                btn.style.color = "white";
                btn.style.border = "none";
                btn.style.borderRadius = "50%";
                btn.style.width = "25px";
                btn.style.height = "25px";
                btn.style.cursor = "pointer";

                btn.onclick = function () {
                    archivos.splice(index, 1);
                    actualizarInput();
                    renderPreview();
                };

                container.appendChild(img);
                container.appendChild(btn);
                preview.appendChild(container);
            };

            reader.readAsDataURL(file);
        });
    }

    function actualizarInput() {
        const dataTransfer = new DataTransfer();
        archivos.forEach(file => {
            dataTransfer.items.add(file);
        });
        input.files = dataTransfer.files;
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const precioInput = document.querySelector('input[name="precio"]');

    if (!precioInput) return;

    function formatearNumero(valor) {
        return valor.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    precioInput.addEventListener("input", function (e) {
        let valor = e.target.value.replace(/\D/g, ""); // solo números

        e.target.value = valor ? formatearNumero(valor) : "";
    });

    // Antes de enviar → quitar puntos
    precioInput.form.addEventListener("submit", function () {
        precioInput.value = precioInput.value.replace(/\./g, "");
    });
});