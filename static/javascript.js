window.onload = function() {
    for (var i = 0; i < 50; i++) {
      var snowflake = document.createElement("div");
      snowflake.classList.add("snowflake");
      snowflake.style.left = Math.random() * 100 + "%";
      snowflake.style.animationDelay = Math.random() * 5 + "s";
      snowflake.style.animationDuration = Math.random() * 10 + 5 + "s";
      snowflake.style.animationTimingFunction = "ease-in-out";
      document.getElementById("snowflakesContainer").appendChild(snowflake);
    }
  };


const menuButton = document.querySelector(".menu-button");
const sidebar = document.querySelector(".sidebar");

menuButton.addEventListener("click", function () {
  sidebar.classList.toggle("open");
});