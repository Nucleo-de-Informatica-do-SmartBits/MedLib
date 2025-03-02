document.querySelector('.submit-btn').addEventListener('click',async function(){let button=this;let existingLoader=button.querySelector('.loader');if(existingLoader){existingLoader.remove();}
let loader=document.createElement('span');loader.classList.add('loader');loader.style.marginLeft='8px';loader.innerHTML='⏳';button.textContent='Enviando';button.appendChild(loader);const commentInput=document.querySelector('#js-comment-input');const content=commentInput.value.trim();if(!content){alert("O comentário não pode estar vazio.");resetButton(button);return;}
const csrfToken=document.querySelector('#csrf_token').value;try{const response=await fetch("/library/add-comment/",{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':csrfToken},body:JSON.stringify({book_slug:'',content:content})});if(response.ok){const data=await response.json();setTimeout(()=>{resetButton(button);const p=document.querySelector("#no-comments")
if(p){p.remove()}
document.querySelector('#js-comments').insertAdjacentHTML('afterbegin',`
                <div class="comment">
                  <div class="comment-info">
                    <h3 class="comment-author" data-user-id="${data.userId}">${data.username}</h3>
                    <span style="color: gray;">${data.created_at}</span>
                  </div>
                  <p class="comment-text">${data.content}</p>
                </div>
                `)},1000)
commentInput.value="";}else{const errorData=await response.json();alert("Erro: "+(errorData.error||"Não foi possível enviar o comentário."));}}catch(error){alert("Erro ao enviar comentário. Tente novamente.");}});function resetButton(button){button.textContent='Enviar';};