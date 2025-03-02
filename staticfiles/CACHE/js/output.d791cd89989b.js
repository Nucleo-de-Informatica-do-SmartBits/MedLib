const processNumber=document.querySelector("#num-process")
processNumber.addEventListener("input",(event)=>{const value=event.data
if(!Number(value)&&Number(value)!==0){processNumber.value=processNumber.value.replace(value,"")}
if(processNumber.value.length>4){processNumber.value=processNumber.value.slice(0,4)}
if(value===" "){processNumber.value=processNumber.value.replace(value,"")}
if(processNumber.value.length>0){processNumber.style.fontSize='25px'}else{processNumber.style.fontSize='15px'}});