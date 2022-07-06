/* Navigation */
let burgerMenu = document.querySelector('.burger_menu');
let navigation = document.querySelector('.nav_list');

burgerMenu.addEventListener('click', slideMenu);

function slideMenu() {
    burgerMenu.classList.toggle('switch_menu');
    navigation.classList.toggle('toggle_navigation');
}
var fullbox = document.getElementById("fullbox");
var fullimg = document.getElementById("fullImg");
function openfull(pic){
    fullbox.style.display = "flex";
    fullimg.src = pic;
}
function closefull(){
    fullbox.style.display = "none";
}

/*Anaimate on scroll config */
AOS.init(
    {
        delay: 50,
    }
);