let pdfDoc = null,
  pageNum = 1,
  canvas = document.getElementById('pdf-render'),
  ctx = canvas.getContext('2d'),
  totalPages = 0

/*function renderPage(num) {
  pdfDoc.getPage(num).then((page) => {
    let viewport = page.getViewport({ scale: 1.5 })
    canvas.height = viewport.height
    canvas.width = viewport.width
    let renderContext = { canvasContext: ctx, viewport: viewport }
    page.render(renderContext)
    document.getElementById('current-page').textContent = num
  })
}*/

function renderPage(num) {
  pdfDoc.getPage(num).then((page) => {
    let viewport = page.getViewport({ scale: 1.2 }); // Ajusta o zoom do PDF
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    let renderContext = { canvasContext: ctx, viewport: viewport };
    page.render(renderContext);
    document.getElementById("current-page").textContent = num;
  });
}

function nextPage() {
  if (pageNum < totalPages) {
    pageNum++
    renderPage(pageNum)
  }
}

function prevPage() {
  if (pageNum > 1) {
    pageNum--
    renderPage(pageNum)
  }
}

pdfjsLib.getDocument(url).promise.then((pdfDoc_) => {
  pdfDoc = pdfDoc_
  totalPages = pdfDoc.numPages
  document.getElementById('total-pages').textContent = totalPages
  renderPage(pageNum)
})

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') nextPage()
  if (e.key === 'ArrowLeft') prevPage()
})

let timerElement = document.getElementById('timer')
let userTime = 0

Swal.fire({
  title: 'Qual o tempo de leitura?',
  input: 'number',
  inputLabel: 'Informe o tempo em minutos',
  inputValue: 30,
  showCancelButton: true,
  confirmButtonText: 'Confirmar',
  cancelButtonText: 'Cancelar',
  allowOutsideClick: false,
  inputValidator: (value) => {
    if (!value || value <= 0) return 'Informe um tempo válido!'
  }
}).then((result) => {
  if (result.isConfirmed) {
    userTime = parseInt(result.value) * 60
    timerElement.style.display = 'block'
    startTimer(userTime)
  } else {
    window.location.href = `/library/book/${slug}/${isbn}/`
  }
})

function startTimer(time) {
  let remainingTime = time
  let countdownInterval = setInterval(() => {
    remainingTime--
    let minutesLeft = Math.floor(remainingTime / 60)
    let secondsLeft = remainingTime % 60
    timerElement.textContent = `${minutesLeft.toString().padStart(2, '0')}:${secondsLeft.toString().padStart(2, '0')}`
    if (remainingTime <= 0) {
      clearInterval(countdownInterval)
      Swal.fire({
        title: 'Tempo esgotado!',
        text: 'O tempo de leitura acabou!',
        icon: 'warning',
        confirmButtonText: 'Ok',
        allowOutsideClick: false
      }).then(() => {
        window.location.href = '/library/'
      })
    }
  }, 1000)
}

document.getElementById('stop-reading').addEventListener('click', () => {
  Swal.fire({
    title: 'Tem certeza que quer parar de ler?',
    showCancelButton: true,
    confirmButtonText: 'Confirmar',
    cancelButtonText: 'Cancelar',
    allowOutsideClick: false
  }).then((result) => {
    if (result.isConfirmed) window.location.href = '/library/'
  })
})

document.addEventListener("DOMContentLoaded", function () {
  const title = document.getElementById("bookTitle");

  title.addEventListener("click", function () {
    // Alternar entre truncado e completo
    if (title.style.whiteSpace === "nowrap") {
      title.style.whiteSpace = "normal"; // Exibe todo o texto
      title.style.overflow = "visible";
    } else {
      title.style.whiteSpace = "nowrap"; // Volta a truncar
      title.style.overflow = "hidden";
    }
  });
});