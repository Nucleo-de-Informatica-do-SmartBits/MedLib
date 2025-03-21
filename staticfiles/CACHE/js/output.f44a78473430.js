document.querySelectorAll('.nav-text').forEach(e=>{e.style.fontWeight='400'})
document.addEventListener('htmx:configRequest',(event)=>{const xhr=event.detail.headers
xhr['X-CSRFToken']=document.querySelector('meta[name="csrf-token"]').getAttribute('content')});