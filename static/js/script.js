const file = document.querySelector('input[type="file"');

file.addEventListener("change", () => {
  document.querySelector(".file-name").textContent = 'Загружено'
});

const burger = document.querySelector(".navbar-burger");
const menu = document.querySelector(".navbar-menu");

burger.addEventListener("click", () => {
  burger.classList.toggle("is-active");
  menu.classList.toggle("is-active");
});
