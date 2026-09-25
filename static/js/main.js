// =============================
// AUTO-HIDE FLASH MESSAGES
// =============================

document.addEventListener("DOMContentLoaded", function () {

    const messages = document.querySelectorAll(
        ".flash-message"
    );

    messages.forEach(function (message) {

        setTimeout(function () {

            message.style.transition =
                "opacity 0.5s ease";

            message.style.opacity = "0";

            setTimeout(function () {

                message.remove();

            }, 500);

        }, 3000);

    });

});
// =============================
// MOBILE NAVBAR
// =============================

document.addEventListener("DOMContentLoaded", function () {

    const menuButton = document.getElementById(
        "mobileMenuButton"
    );

    const mainNav = document.getElementById(
        "mainNav"
    );


    if (!menuButton || !mainNav) {
        return;
    }


    menuButton.addEventListener(
        "click",
        function () {

            mainNav.classList.toggle(
                "mobile-open"
            );

            menuButton.classList.toggle(
                "menu-active"
            );


            const isOpen =
                mainNav.classList.contains(
                    "mobile-open"
                );


            menuButton.setAttribute(
                "aria-expanded",
                isOpen
            );

        }
    );


    // Close the menu after clicking a link

    const navLinks =
        mainNav.querySelectorAll("a");


    navLinks.forEach(function (link) {

        link.addEventListener(
            "click",
            function () {

                mainNav.classList.remove(
                    "mobile-open"
                );

                menuButton.classList.remove(
                    "menu-active"
                );

                menuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );

            }
        );

    });

});