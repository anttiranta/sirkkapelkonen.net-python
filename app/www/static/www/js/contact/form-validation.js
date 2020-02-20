$(document).ready(function () {
    try {
        $("#yhteys_lomake").validate()({
            debug: false,
            rules: {
                name: "required",
                email: {
                    required: true,
                    email: true
                },
                message: "required"
            },
            messages: {
                name: "Nimi täytyy antaa.",
                email: "Sähköposti täytyy antaa.",
                message: "Viesti täytyy antaa."
            }
        });
    } catch(exception) {
        if (!(exception instanceof TypeError)) {
            console.log("Failed to validate contact form. Error: " + exception.message)
        }
    }
});