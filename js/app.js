/* Navigation */
let burgerMenu = document.querySelector('.burger_menu');
let navigation = document.querySelector('.nav_list');

burgerMenu.addEventListener('click', slideMenu);

function slideMenu() {
    burgerMenu.classList.toggle('switch_menu');
    navigation.classList.toggle('toggle_navigation');
}

/*Anaimate on scroll config */
AOS.init(
    {
        delay: 50,
    }
);