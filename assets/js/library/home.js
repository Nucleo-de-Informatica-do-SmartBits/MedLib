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

document.querySelectorAll(".card-book")
    .forEach(card => {
        card.addEventListener('click', (e) => {
            const slug = card.dataset.bookSlug
            const isbn = card.dataset.bookIsbn

            if (slug) {
                window.location.href = '/library/book/' + slug + '/' + isbn + '/'
            }
        })

    });

document.querySelector('.js-suggestion-btn')
    .addEventListener('click', async () => {
        const button = document.querySelector('.js-suggestion-btn');
        const suggestionInput = document.querySelector('#suggestion-textarea');
        const suggestion = suggestionInput.value;
        const CSRFToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const successSVG = `<svg xmlns="http://www.w3.org/2000/svg" style="color: green;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>`;
        const errorSVG = `<svg xmlns="http://www.w3.org/2000/svg" style="color: red;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>`;


        button.disabled = true;
        button.classList.add('loading');
        button.innerHTML = '';

        setTimeout(async () => {
            try {
                const response = await fetch('/library/add-suggestion/', {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Csrftoken': CSRFToken
                    },
                    body: JSON.stringify({ content: suggestion })
                });

                if (response.ok) {
                    button.classList.remove('loading');
                    button.innerHTML = 'Enviado! ' + successSVG;
                    setTimeout(() => {
                        button.innerHTML = 'Enviar';
                        button.disabled = false;
                    }, 3000);
                } else {
                    throw new Error('Erro no envio');
                }
            } catch (error) {
                button.classList.remove('loading');
                button.innerHTML = 'Preencha o campo acima! ' + errorSVG;
                setTimeout(() => {
                    button.innerHTML = 'Enviar';
                    button.disabled = false;
                }, 3000);
            }
        }, 1000);
        suggestionInput.value = ''
    })

document.getElementById('search-input').addEventListener('input', async function (e) {
    const input = e.target.value.trim();
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('results-container');
    const searchResults = document.getElementById('search-results');

    if (input === '') {
        resultsContainer.innerHTML = '';
        searchResults.classList.add('hidden');
        return;
    }

    try {
        resultsContainer.innerHTML = '';
        loader.classList.remove('hidden');
        searchResults.classList.remove('hidden');

        const response = await fetch(`/library/search-for-books/?q=${encodeURIComponent(input)}`);
        const data = await response.json();

        setTimeout(() => {
            loader.classList.add('hidden');
            resultsContainer.innerHTML = '';

            if (data.length > 0) {
                data.forEach(book => {
                    const bookElement = document.createElement('div');
                    bookElement.classList.add('result-item', 'fade-in');
                    bookElement.innerHTML = `
                        <a href="/library/book/${book.slug}/${book.isbn}/" class="s-results">
                            ${book.title}
                        </a>
                    `;
                    resultsContainer.appendChild(bookElement);
                });
            } else {
                resultsContainer.innerHTML = '<div class="p-2 text-center text-white-500">Sem resultados para "' + input + '"</div>';
            }
        }, 1000);
    } catch (error) {
        console.error("Erro ao buscar livros:", error);
        resultsContainer.innerHTML = '<div class="p-2 text-red-500">Erro ao buscar livros.</div>';
        loader.classList.add('hidden');
    }
});


document.body.addEventListener('click', (e) => {
    const resultsContainer = document.getElementById('results-container');
    const searchResults = document.getElementById('search-results');
    const input = document.querySelector('#search-input')

    if (
        e.target === input ||
        e.target === searchResults ||
        e.target === resultsContainer ||
        e.target.className === 'result-item fade-in') {
        return
    }

    if (resultsContainer && searchResults) {
        input.value = ''
        resultsContainer.innerHTML = '';
        searchResults.classList.add('hidden');
    }
})