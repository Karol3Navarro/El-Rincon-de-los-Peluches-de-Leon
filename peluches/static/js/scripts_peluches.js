new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,

    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },

    autoplay: {
        delay: 2000,
        disableOnInteraction: false,
    },

    breakpoints: {
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
        1200: { slidesPerView: 5 },
    }
});

document.addEventListener("DOMContentLoaded", function(){
    new Swiper(".mySwiperPeluche", {
        slidesPerView: 1,
        spaceBetween: 10,
        loop: true,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
    });
});

// document.addEventListener("DOMContentLoaded", function () {
//     const btn = document.getElementById("verMasCategorias");
//     if (!btn) return;

//     const items = document.querySelectorAll(".categoria-item");
//     const STORAGE_KEY = "categorias_expandidas";

//     let expanded = localStorage.getItem(STORAGE_KEY) === "true";

//     function applyState() {
//         items.forEach((el, index) => {
//             if (index >= 3) {
//                 el.classList.toggle("hidden-cat", !expanded);
//             }
//         });

//         btn.textContent = expanded ? "Ver menos" : "Ver más";
//     }

//     applyState();

//     btn.addEventListener("click", function () {
//         expanded = !expanded;
//         localStorage.setItem(STORAGE_KEY, expanded);
//         applyState();
//     });
// });
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