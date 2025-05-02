const menu = document.querySelector('.menu');
const aside = document.querySelector('#aside');
const removeAside = document.querySelector('#remove_aside');
const profileDropdown = document.querySelector('.myprofile');
const headerProfile = document.querySelector('#display_profile');
const removeProfile = document.querySelector('.remove_profile');


headerProfile.addEventListener('click', () => {
    profileDropdown.classList.add('myprofileshow');
    profileDropdown.style.transition = '0.6s ease forwards';
})

removeProfile.addEventListener('click', () => {
    profileDropdown.classList.remove('myprofileshow');
    profileDropdown.style.transition = '0.6s ease forwards';
})

menu.addEventListener('click', () => {
    aside.classList.add('asideshow');
    aside.style.transition = '0.6s ease forwards';
})

removeAside.addEventListener('click', () => {
    aside.classList.remove('asideshow');
    aside.style.transition = '0.6s ease forwards';
})

// writing the javscript for the  search icon redirection

const search_svg = document.querySelector('.search_svg');
search_svg.addEventListener('click', () => {
    window.location.href = "/eduklinikapp/search.html";
    search_svg.style.transition = "all ease 0.4s";
});

// the code for the whatsapp logo at the bottom corner of the site
function opacity() {
    const whatsapp = document.querySelector('.whatsapp_message');
    window.addEventListener('scroll', () => {
        whatsapp.classList.add('.whatsapp_message_opacity');
    })
}
opacity();

// omo guy that above javscript code no dey work o . I know even know y. check am
// my system just dey do anyhow nii guy . i swear i gats buy macbook seh





