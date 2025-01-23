let currentIndex = 0;
const images = document.querySelectorAll("#image-slider img");

const frasesArray = [
    "\"A leitura é a chave para abrir portas para o mundo do conhecimento e da imaginação.\"",
    "\"A leitura nos dá asas para voar nas mais diversas imaginações.\"",
    "\"Cada livro é uma viagem esperando para ser vivida\"",
]

const totalImages = images.length;

function changeImage() {
    let text = document.querySelector('#text')

    currentIndex = (currentIndex + 1) % totalImages;

    const offset = -currentIndex * 100;
    document.getElementById("image-slider").style.transform = `translateX(${offset}%)`;

    text.innerText = frasesArray[currentIndex]
}

setInterval(changeImage, 3000);

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = "flex";
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = "none";
}