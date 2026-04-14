
$(document).ready(function() {
    // Mensajes que desaparecen automáticamente
    $("#idMensajes").delay(2000).fadeOut("slow");

    // Previsualizar imágenes seleccionadas
    $("#imagenesInput").on("change", function() {
        $("#preview").html(""); // limpiar previsualización
        let files = this.files;

        for (let i = 0; i < files.length; i++) {
            let reader = new FileReader();
            reader.onload = function(e) {
                let img = $("<img>")
                    .attr("src", e.target.result)
                    .css({
                        "width": "120px",
                        "margin": "5px",
                        "border": "1px solid #ccc"
                    });
                $("#preview").append(img);
            }
            reader.readAsDataURL(files[i]);
        }
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
    const calendarEl = document.getElementById('calendar');

    if (!calendarEl) return; // evita errores en otras páginas

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',

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