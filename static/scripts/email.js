
(() => {
    // https://dashboard.emailjs.com/admin/integration
    emailjs.init('user_KawIFAZeIVDQAGA5WIFg4');
})();

window.onload = function () {
    document.getElementById('contact-form').addEventListener('submit', function (event) {
        event.preventDefault();
        // generate a five digit number for the contact_number variable
        this.contact_number.value = Math.random() * 100000 | 0;
        // these IDs from the previous steps
        emailjs.sendForm("service_h29703b","template_bs0x3fa", this)
            .then(function () {
                console.log('SUCCESS!');
                alert("Thank you for the messege! We will review your submission shortly.")
            }, function (error) {
                console.log('FAILED...', error);
                alert("Ooops... Something went wrong. Please try again later.")
            });
    });
}
