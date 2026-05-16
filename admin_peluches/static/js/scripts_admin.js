document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll('.alert:not(.alert-reporte)');

    if (!alerts.length) return;

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('fade');

            setTimeout(() => {
                alert.remove();
            }, 500);

        }, 3000);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const botones = document.querySelectorAll(".btnEliminarImg");
    const btnConfirmar = document.getElementById("btnConfirmarEliminarImg");

    if (!botones.length || !btnConfirmar) return;

    botones.forEach(btn => {
        btn.addEventListener("click", function () {
            const id = this.dataset.id;
            btnConfirmar.href = `/admin_peluches/peluche_imagen_del/${id}/`;
        });
    });
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
    const btnMes = document.getElementById('btnMes');
    const formMes = document.getElementById('formMes');

    if (btnMes && formMes) {
        btnMes.addEventListener('click', function (e) {
            e.preventDefault();
            formMes.classList.toggle('d-none');
            formMes.classList.toggle('show');
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) return; // evita errores en otras páginas

    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'es',
        timeZone: 'America/Santiago',
        firstDay: 1,
        initialView: window.innerWidth < 768 ? 'listWeek' : 'dayGridMonth',
        weekNumbers: false,
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
                "📅 " + fecha.toLocaleDateString('es-CL') +
                " ⏰ " + fecha.toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' });

            document.getElementById("modalLugar").innerText =
                "📍 " + (info.event.extendedProps.description || "No definido");

            document.getElementById("modalImagen").src =
                info.event.extendedProps.image || "";

            const form = document.getElementById("formEntregado");
            if (form) {
                form.action = `/admin_peluches/entregado/${id}/`;
            }

            const btnVer = document.getElementById("btnVerPeluche");
            if (btnVer) {
                btnVer.href = `/admin_peluches/peluche/${id}/`;
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

document.addEventListener("DOMContentLoaded", function () {

    const modalEl = document.getElementById("pelucheModal");
    if (!modalEl) return;

    // 🔥 UNA sola instancia
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

    document.querySelectorAll(".fila-peluche").forEach(fila => {
        fila.addEventListener("click", function () {

            document.getElementById("modalNombre").innerText = this.dataset.nombre;
            document.getElementById("modalFecha").innerText = this.dataset.fecha;

            document.getElementById("modalEstado").innerText =
                this.dataset.entregado === "True" ? "Entregado" : "Pendiente";

            document.getElementById("modalPrecio").innerText = this.dataset.precio;

            // 🖼️ Imagen
            const img = document.getElementById("modalImagen");
            if (this.dataset.imagen) {
                img.src = this.dataset.imagen;
                img.style.display = "block";
            } else {
                img.style.display = "none";
            }

            // 🔗 Botón ver peluche
            const btn = document.getElementById("btnVerPeluche");
            btn.href = `/admin_peluches/peluche/${this.dataset.id}/`;

            // 🔥 reutiliza el modal
            modal.show();
        });
    });

});

document.addEventListener('hidden.bs.modal', function (event) {

    // 🔥 Quita el foco del elemento activo (ej: botón cerrar)
    if (document.activeElement) {
        document.activeElement.blur();
    }

    // 🔥 Limpieza por si Bootstrap deja basura
    document.body.classList.remove('modal-open');
    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());

});

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("verMasCategorias");
    const container = document.getElementById("categorias-lista");

    if (!btn || !container) return;

    const items = document.querySelectorAll(".categoria-item");
    const STORAGE_KEY = "categorias_expandidas";

    let expanded = localStorage.getItem(STORAGE_KEY) === "true";

    function applyState() {
        // mostrar/ocultar items
        items.forEach((el, index) => {
            if (index >= 3) {
                el.classList.toggle("hidden-cat", !expanded);
            }
        });

        // activar scroll SOLO cuando está expandido
        container.classList.toggle("expanded", expanded);

        btn.textContent = expanded ? "Ver menos" : "Ver más";
    }

    applyState();

    btn.addEventListener("click", function () {
        expanded = !expanded;
        localStorage.setItem(STORAGE_KEY, expanded);
        applyState();
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const botones = document.querySelectorAll(".btnEliminarCategoria");
    const btnConfirmar = document.getElementById("btnConfirmarEliminarCategoria");

    if (!botones.length || !btnConfirmar) return;

    const modal = new bootstrap.Modal(document.getElementById("modalEliminarCategoria"));

    botones.forEach(btn => {
        btn.addEventListener("click", function () {

            const id = this.dataset.id;

            btnConfirmar.href = `/admin_peluches/categoria/eliminar/${id}/`;

            modal.show();
        });
    });

});