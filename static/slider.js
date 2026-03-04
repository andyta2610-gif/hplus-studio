var slides = document.querySelectorAll(".slide");
var index = 0;

function nextSlide() {
    slides[index].classList.remove("active");
    index = (index + 1) % slides.length;
    slides[index].classList.add("active");
}

setInterval(nextSlide, 4500);