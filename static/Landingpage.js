let menu =document.querySelector('#menu-icon');
let navbar =document.querySelector('.navbar');

menu.onclick = () =>{
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('active');

}

Window.onscroll = () =>{
    menu.classList.remove('bx-x');
    navbar.classList.remove('active');
}

//Typing twext code
var typed = new Typed('.multiple-text', {
    strings: ['One Click','Connect', 'Register','Train' ,'Build'],
    typeSpeed: 60,
    backSpeed: 60,
    backDelay:1000,
    loop:true
  });

function Service_ai() {
    window.open("/Service-ai", "_blank");  // Ab Flask ka index.html naye tab me open hoga
}
