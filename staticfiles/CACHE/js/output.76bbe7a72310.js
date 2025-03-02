PDFObject.embed('','#pdf-view')
let seconds=0
let minutes=0
let timerElement=document.getElementById('timer')
let userTime=0
Swal.fire({title:'Qual o tempo de leitura?',input:'text',inputLabel:'Informe o tempo em minutos',inputValue:30,showCancelButton:true,confirmButtonText:'Confirmar',cancelButtonText:'Cancelar',backdrop:'static',allowOutsideClick:false,inputValidator:(value)=>{if(!value||value<=0){return'Por favor, informe um tempo válido!'}else if(value>60){return'Por favor, informe um tempo menor!'}}}).then((result)=>{if(result.isConfirmed){document.querySelector('.logo-container').innerHTML=``
document.querySelector('#timer-sec').style.visibility='visible'
setTimeout(()=>{userTime=parseInt(result.value)*60
startTimer(userTime)},1000)
document.querySelector('nav').style.backgroundColor='#3DB1C8'
document.querySelector('nav').style.height='70px'
document.querySelector('.div-middle').style.display='flex'
document.querySelector('.div-middle').style.flexDirection='column'
document.querySelector('.div-middle').innerHTML=`<span style="color: white;font-size: 20px;">Você está em modo de leitura.</span><span style="text-align: center;font-style: italic;color: white;">Mantenha o foto, e aproveite!</span>`
document.querySelector('.user-img').innerHTML=`
                    <button style="background-color: red;color: white;border-radius: 5px;width: 80px;padding: 10px;" id="btn-stop">Parar</button>
                `
document.querySelector('#btn-stop').addEventListener('click',()=>{let modal=Swal.fire({title:'Tem certeza que quer parar de ler?',showCancelButton:true,confirmButtonText:'Confirmar',cancelButtonText:'Cancelar',backdrop:'static',allowOutsideClick:false})
modal.then((result)=>{if(result.isConfirmed){window.location.href="/library/"}})})}else{window.location.href="/library/"}})
function startTimer(time){let remainingTime=time
let countdownInterval=setInterval(function(){remainingTime--
let minutesLeft=Math.floor(remainingTime/60)
let secondsLeft=remainingTime%60
timerElement.textContent=(minutesLeft<10?'0':'')+minutesLeft+':'+(secondsLeft<10?'0':'')+secondsLeft
if(remainingTime<=0){clearInterval(countdownInterval)
Swal.fire({title:'Tempo esgotado!',text:'O tempo de leitura acabou!',icon:'warning',confirmButtonText:'Ok',backdrop:'static',allowOutsideClick:false}).then(()=>{window.location.href="/auth/logout/"})}},1000)};