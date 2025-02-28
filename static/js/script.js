function updateFileName() {
  const input = document.querySelector('input[type="file"]');
  console.log(input);

  const fileName =
    input.files.length > 0 ? input.files[0].name : "Файл не выбран";
  console.log(fileName);

  input.textContent = fileName;
}

const burger = document.querySelector(".navbar-burger");
const menu = document.querySelector(".navbar-menu");

burger.addEventListener("click", () => {
  burger.classList.toggle("is-active");
  menu.classList.toggle("is-active");
});
