document.querySelector('#js-see-more-btn')
    .addEventListener('click', (event) => {
        document.querySelector('#objective').scrollIntoView({
            behavior: 'smooth',
            block: 'nearest'
        })
    })

