const menu = document.querySelector('.hamburger-menu');
const nav = document.querySelector('.responsive-dropdown');
const removeNav = document.querySelector('.remove_nav');
//adding the event listener

menu.addEventListener('click', () => {
    nav.classList.add('nav_show');
})
removeNav.addEventListener('click', () => {
    nav.classList.remove('nav_show');
})

//typewriter javascript thart is the logic behind the the typewriter knowledge
const text = document.querySelector('.text');

const textLoad = () => {
    setTimeout(() => {
        text.textContent = "Eduklinik Learning Nexus.";
    }, 0);
    setTimeout(() => {
        text.textContent = "\"The Centre of excellence\".";
        text.style.color = 'black';
    }, 4000);
    setTimeout(() => {
        text.textContent = "\"The Citadel of Innovation\".";
        text.style.color = 'white';
    }, 8000);
    text.style.color = 'gold';
}
//calling the functions
textLoad();
setInterval(textLoad, 12000);

//login and register forms showing the containers , calling the elements and assigning a variable to each

const loginForm = document.querySelector('.form');
const regForm = document.querySelector('.form_2');
const loginBtn = document.querySelector('.login');
const regBtn = document.querySelector('.register');
const submitBtn = document.querySelector('.formBtn');
const removeLoginForm = document.querySelector('.remove_form');
const removeRegForm = document.querySelector('.remove_form_2');
const registerSubmitBtn = document.querySelector('.form_2_register');
const loginRedirect = document.querySelector('.login_redirect');
const registerRedirect = document.querySelector('.Register_redirect');
const enrol_btn = document.querySelector('#enrol_btn');
const enrol_btn_two = document.querySelector('#enrol_btn2');

//calling the event listener for each called elements
// this is the eventlisteners that makes it possible for the functionality of the above called elements{the login stuff and the register stuff}
enrol_btn.addEventListener('click', () => {
    regForm.classList.add('register_show');
})
enrol_btn_two.addEventListener('click', () => {
    regForm.classList.add('register_show');
})
loginBtn.addEventListener('click', () => {
    loginForm.classList.add('login-show');
})
submitBtn.addEventListener('click', () => {
    loginForm.classList.remove('login-show');
})
removeLoginForm.addEventListener('click', () => {
    loginForm.classList.remove('login-show');
})
removeRegForm.addEventListener('click', () => {
    regForm.classList.remove('register_show');
})
regBtn.addEventListener('click', () => {
    regForm.classList.add('register_show');
})
registerSubmitBtn.addEventListener('click', () => {
    regForm.classList.remove('register_show');
})

//redirecting the small hyper redirection links

loginRedirect.addEventListener('click', () => {
    loginForm.classList.add('login-show');
    regForm.classList.remove('register_show');
    style.transition = "all 0.5s ease";
})
registerRedirect.addEventListener('click', () => {
    regForm.classList.add('register_show');
    loginForm.classList.remove('login-show');
    style.transition = "all 0.5s ease";
})

//redirecting the login and register button

//const loginServices = document.querySelector('.login_services');
//loginServices.addEventListener('click', () => {
   // loginForm.classList.add('login-show');
//})

//const registerServices = document.querySelector('.register_services');
//registerServices.addEventListener('click', () => {
 //   regForm.classList.add('register_show');
//})

/* calling the automatic slider for the services section */

const slideOne = document.querySelector('.services_body_1_content');
const slideTwo = document.querySelector('.services_body_2_content');
const slideThree = document.querySelector('.services_body_3_content');
const slideFour = document.querySelector('.services_body_4_content');


/*the following is the code for the intersection oberver of some particular sections on the home page */
// normally this work suppose cost reach like 6 million

function intersectionObserver1() {
    const choose = document.querySelector('.choose_text');
    const interPosition = choose.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 2;
    if (interPosition < screenPosition) {
        choose.classList.add("choose_intersect");
    }
    else {
        choose.classList.remove("choose_intersect");
    }
}
window.addEventListener("scroll", intersectionObserver1);

function intersectionObserverImage() {
    const chooseImage = document.querySelector('.choose_image');
    const interPosition = chooseImage.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 2;
    if (interPosition < screenPosition) {
        chooseImage.classList.add("choose_image_intersect");
    }
    else {
        chooseImage.classList.remove("choose_image_intersect");
    }
}
window.addEventListener("scroll", intersectionObserverImage);

function intersectionObserver2() {
    const programSectOne = document.querySelector('.program_sect_1');
    const interPosition = programSectOne.getBoundingClientRect().top;
    const screenPosition = window.innerHeight;
    if (interPosition < screenPosition) {
        programSectOne.classList.add("program_intersect");
    }
    else {
        programSectOne.classList.remove("program_intersect");
    }
}
window.addEventListener("load", intersectionObserver2);

function intersectionObserver3() {
    const programSectTwo = document.querySelector('.program_sect_2');
    const interPosition = programSectTwo.getBoundingClientRect().top;
    const screenPosition = window.innerHeight;
    if (interPosition < screenPosition) {
        programSectTwo.classList.add("program_intersect_2");
    }
    else {
        programSectTwo.classList.remove("program_intersect_2");
    }
}
window.addEventListener("load", intersectionObserver3);
// calling a function for the observer of the tutor section

function intersectionObserver4() {
    const tutors = document.querySelector('.tutors_content');
    const interPosition = tutors.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 2;
    if (interPosition < screenPosition) {
        tutors.classList.add("tutors_content_intersect");
    }
    else {
        tutors.classList.remove("tutors_content_intersect");
    }
}
window.addEventListener("scroll", intersectionObserver4);

function intersectionObserver5() {
    const service = document.querySelector('.services');
    const interPosition = service.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 2;
    if (interPosition < screenPosition) {
        service.classList.add("service_intersect");
    }
    else {
        service.classList.remove("service_intersect");
    }
}
window.addEventListener("scroll", intersectionObserver5);

function intersectionObserver6() {
    const video = document.querySelector('.video');
    const interPosition = video.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 2;
    if (interPosition < screenPosition) {
        video.classList.add("video_intersect");
    }
    else {
        video.classList.remove("video_intersect");
    }
}
window.addEventListener("scroll", intersectionObserver6);

function intersectionObserver7() {
    const partner = document.querySelector('.partners');
    const interPosition = partner.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 2;
    if (interPosition < screenPosition) {
        partner.classList.add("partners_intersect");
    }
    else {
        partner.classList.remove("partners_intersect");
    }
}
window.addEventListener("scroll", intersectionObserver7);

// calling the event listener for the contact footer animation section 
const contactActive = document.querySelector('.contact_active');
const contactFooter = document.querySelector('.contacts');
contactActive.addEventListener('click', () => {
    contactFooter.classList.add('contacts_animation');
})

/* writing the slider effect*/

const slides = document.querySelectorAll('.slide_services');
let currentSlide = 0;
const showSlide = (index) => {
    slides.forEach((slide, i) => {
        slide.style.display = (i === index) ? 'block' : 'none';
    });
};
const nextSlide = () => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
};
function showNext() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
    slides.style.transition = 'all 1s forwards';
}
function showPrev() {
    currentSlide = (currentSlide - 1) % slides.length;
    showSlide(currentSlide);
}
//call each function after each assignment
showPrev();
showNext();
showSlide(currentSlide);
setInterval(nextSlide, 3000);

//short and precise no long story nor indefinite thinking that might doubt your intelligence
/* this is the end of the slider effect */
































































































































































