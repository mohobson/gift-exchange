const menuButton = document.querySelector(".menu-button");
const sidebar = document.querySelector(".sidebar");
const sidebarContent = document.querySelector(".sidebar-content");
const blockContent = document.querySelector(".block-content");

menuButton.addEventListener("click", () => {
  sidebar.classList.toggle("show");
  sidebarContent.classList.toggle("show");
  blockContent.classList.toggle("hidden");
});