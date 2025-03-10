new TypeIt('#typewriter', {
    strings: 'MedLib',
    speed: 75,
    loop: false,
    cursor: false
}).go()

const profileImg = document.getElementById('profile-img')
const profileMenu = document.getElementById('profile-menu')

profileImg.addEventListener('click', () => {
    if (profileMenu.classList.contains('hidden')) {
        profileImg.classList.add('active')
        profileMenu.classList.remove('hidden')
        setTimeout(() => {
            profileMenu.classList.remove('scale-95', 'opacity-0')
            profileMenu.classList.add('scale-100', 'opacity-100')
        }, 10)
    } else {
        profileImg.classList.remove('active')
        profileMenu.classList.remove('scale-100', 'opacity-100')
        profileMenu.classList.add('scale-95', 'opacity-0')
        setTimeout(() => profileMenu.classList.add('hidden'), 200)
    }
})

document.addEventListener('click', (event) => {
    if (!profileImg.contains(event.target) && !profileMenu.contains(event.target)) {
        profileMenu.classList.remove('scale-100', 'opacity-100')
        profileMenu.classList.add('scale-95', 'opacity-0')
        profileImg.classList.remove('active')
        setTimeout(() => profileMenu.classList.add('hidden'), 200)
    }
})