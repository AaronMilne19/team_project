(() => {
    // https://dashboard.emailjs.com/admin/integration
    emailjs.init('user_AsFKI2VSAXzKBbR4gYrkW');
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
                var successMsg = document.getElementById('alert-suc')
                successMsg.classList.remove('hide-alert');
                console.log('SUCCESS!');
            }, function (error) {
                var errorMsg = document.getElementById('alert-err');
                errorMsg.classList.remove('hide-alert');
                console.log('FAILED...', error);
            });
    });
}
