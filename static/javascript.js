const menuButton = document.querySelector(".menu-button");
const sidebar = document.querySelector(".sidebar");

menuButton.addEventListener("click", () => {
  sidebar.classList.toggle("show");
});