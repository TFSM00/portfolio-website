const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const header = document.querySelector('#header');
const headerHeight = window.getComputedStyle(header).getPropertyValue('height');
document.documentElement.style.setProperty('--header-height', headerHeight);

const toastTrigger = document.getElementById('clipBtn')
const toast = document.getElementById('clip')



function copyToClipboard() {
    const email = "tiagomoreira317@gmail.com";
    navigator.clipboard.writeText(email)
        .catch(err => {
            console.error("Failed to copy text: " + err);
        });
};

function showHide(id, state) {
    let element = document.querySelector(id)
    if (state == "show") {
        element.classList.add("show");
        element.classList.remove("hide");
    } else {
        element.classList.remove("show");
        element.classList.add("hide");
    };
};

$(document).ready(function() {
    // Add click event handler to the button
    $('#clipBtn').click(function() {
        // Show the tooltip
        showHide('#clip', "show");
        // Optional: Hide the tooltip after a certain time (e.g., 2 seconds)
        setTimeout(function() {
            showHide('#clip', "hide");
        }, 2000);
    });
});

// $(document).ready(function() {
//     // Initialize the tooltip
//     $('#clip').tooltip();
// });

