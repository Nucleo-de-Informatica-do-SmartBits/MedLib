document.querySelector('#profile-photo-upload')
    .addEventListener('input', (e) => {
        const file = e.target.files[0];
        
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(event) {
                document.querySelector('#profile-photo-preview')
                    .setAttribute('src', event.target.result);
            };
            
            reader.readAsDataURL(file); 
        }
    });
document.querySelector('#js-eye')
    .addEventListener('click', (e) => {
        const processNumberInput = document.querySelector('#process-number')

        if (e.target.classList.contains('bi-eye')) {
            processNumberInput.type = 'text'
            e.target.classList.replace('bi-eye', 'bi-eye-slash')
        } else {
            processNumberInput.type = 'password'
            e.target.classList.replace('bi-eye-slash', 'bi-eye')
        }
    })

document.querySelector('#js-save').addEventListener('click', async (e) => {
    e.preventDefault();

    const formData = new FormData()

    document.querySelectorAll('input, select').forEach(input => {
        const name = input.getAttribute('name') || input.getAttribute('id');
        if (name) {
            if (input.type === 'file') {
                formData.append(name, input.files[0]);
            } else {
                formData.append(name, input.value);
            }
        }
    });

    const response = await fetch(window.location.pathname, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
        body: formData
    })

    window.location.reload(true)
})