// document.addEventListener("DOMContentLoaded", function() {
//     var swiperContainer = document.querySelector(".mySwiper");

//     if (swiperContainer) {
//         var totalSlides = swiperContainer.querySelectorAll(".swiper-slide").length;

//         new Swiper(".mySwiper", {
//             slidesPerView: Math.min(3, totalSlides),
//             spaceBetween: 20,
//             loop: totalSlides > 1,
//             navigation: {
//                 nextEl: ".swiper-button-next",
//                 prevEl: ".swiper-button-prev",
//             },
//             autoplay: {
//                 delay: 2000,
//                 disableOnInteraction: false,
//             },
//             breakpoints: {
//                 640: { slidesPerView: Math.min(1, totalSlides) },
//                 768: { slidesPerView: Math.min(2, totalSlides) },
//                 1024: { slidesPerView: Math.min(3, totalSlides) },
//             }
//         });
//     }
// });

document.addEventListener("DOMContentLoaded", function(){
    new Swiper(".mySwiper", {
        slidesPerView: 4,
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
            1024: {slidesPerView: 4},
            768: {slidesPerView: 2},
            680: {slidesPerView: 1},
        }
    });
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