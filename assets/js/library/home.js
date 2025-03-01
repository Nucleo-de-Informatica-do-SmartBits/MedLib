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


async function get_book_data(url) {
    const api = await fetch(url);
    return api.json();
}

document.querySelectorAll('.card-book')
    .forEach(card => {
        card.addEventListener('click', async () => {
            const data = await get_book_data(card.dataset.apiUrl);

            document.getElementById('book-cover-modal').setAttribute('src', data.cover)
            document.getElementById('modalTitle').textContent = data.title;
            document.getElementById('modalDescription').textContent = data.summary;

            data.authors.forEach(author => {
                document.getElementById('modalAuthors').innerHTML += `
          <div class="author">
            <div class="author-img-div">
            <img src="${author[0]}">
            </div>
            <span>${author[1]}</span>
            </div>
          `
            })

            document.querySelector("#publisher-div").innerHTML =
                `
          <img src="${data.publisher[0]}" style="width: 55px;heigth: 50px;border-radius: 50%;">
          <span>${data.publisher[1]}</span>        
        `
            document.getElementById('modalPages').textContent = data.pages;
            document.getElementById('modalLanguage').textContent = data.language;
            document.getElementById('modalIsbn').textContent = data.isbn;
            document.getElementById('modalEdition').textContent = `${data.edition}ª`;
            document.getElementById('modalPublicationDate').textContent = `Publicado em ${data.publication_date}`;
            document.getElementById('js-read-link').setAttribute('href', data.read_link)

            // document.getElementById('modalCategories').textContent = data.categories.join(', ');
            const modal = document.getElementById('bookModal');
            modal.style.display = "flex";
        });
    });

document.querySelector('.close-btn').addEventListener('click', () => {
    const modal = document.getElementById('bookModal');
    modal.style.display = "none";
});

window.addEventListener('click', (event) => {
    const modal = document.getElementById('bookModal');
    if (event.target === modal) {
        modal.style.display = "none";
    }
});