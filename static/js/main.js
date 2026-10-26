
"use strict";

// CareConnect AI Hospital Contact Manager
// Frontend enhancements for Flask pages.

document.addEventListener("DOMContentLoaded", () => {

    // 1. Automatically dismiss success notifications
    document.querySelectorAll(".alert.success").forEach((alert) => {
        setTimeout(() => {
            alert.remove();
        }, 5000);
    });

    // 2. Prevent accidental double form submission
    document.querySelectorAll("form[method='POST']").forEach((form) => {

        form.addEventListener("submit", (event) => {

            if (!form.checkValidity()) {
                return;
            }

            if (event.defaultPrevented) {
                return;
            }

            // Preserve Delete confirmation behaviour.
            if (form.action.includes("/delete")) {
                return;
            }

            if (form.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

            form.dataset.submitting = "true";

            const button = event.submitter;

            if (button) {
                // Delay disabling to allow submit button's
                // name/value to be included in the POST.
                setTimeout(() => {
                    button.disabled = true;
                    button.textContent = "Processing...";
                }, 0);
            }
        });
    });

    // 3. Trim unnecessary spaces in text fields
    document.querySelectorAll(
        "input[type='text'], input[type='email'], input[type='tel']"
    ).forEach((input) => {

        input.addEventListener("blur", () => {
            input.value = input.value.trim();
        });

    });

    // 4. Normalize email addresses
    document.querySelectorAll("input[type='email']").forEach((input) => {

        input.addEventListener("blur", () => {
            input.value = input.value.trim().toLowerCase();
        });

    });

    // 5. Contact phone number basic validation
    const phoneInputs = document.querySelectorAll(
        "input[name='phone']"
    );

    phoneInputs.forEach((input) => {

        input.addEventListener("input", () => {
            // Allow digits, spaces and international prefix.
            input.value = input.value.replace(/[^\d+\s()-]/g, "");
        });

        input.addEventListener("blur", () => {

            const value = input.value.trim();

            if (!value) {
                input.setCustomValidity("");
                return;
            }

            const digitCount = value.replace(/\D/g, "").length;

            if (digitCount < 7 || digitCount > 15) {
                input.setCustomValidity(
                    "Please enter a valid phone number (7–15 digits)."
                );
            } else {
                input.setCustomValidity("");
            }

        });

        input.addEventListener("input", () => {
            input.setCustomValidity("");
        });

    });

    // 6. Display selected contact information
    const contactSelect = document.querySelector(
        "select[name='contact_id']"
    );

    if (contactSelect) {
        contactSelect.addEventListener("change", () => {
            console.log(
                "Selected contact ID:",
                contactSelect.value
            );
        });
    }

});
