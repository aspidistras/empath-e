/* Helper function to update the call status bar */
function updateCallStatus(status) {
    $("#call-status").attr('placeholder', status);
}

/* Get a Twilio Client token with an AJAX request */
function setup() {
    $.get("/contact/token", {forPage: window.location.pathname}, function(data) {

         // Set up the Twilio Client Device with the token
        Twilio.Device.setup(data.token, {debug: true});
    });

}

/* Callback to let us know Twilio Client is ready */
Twilio.Device.on("ready", function (device) {
    updateCallStatus("Prêt pour l'appel");
});

/* Report any errors to the call status display */
Twilio.Device.on("error", function (error) {
    console.log("ERROR: " + error.message);
});

/* Callback for when Twilio Client initiates a new connection */
Twilio.Device.on("connect", function (connection) {
    // Enable the hang up button and disable the call buttons
    $(".hangup-button").prop("disabled", false);
    $(".call-button").prop("disabled", true);
    $(".answer-button").prop("disabled", true);

    updateCallStatus("Appel en cours");
});

/* Callback for when a call ends */
Twilio.Device.on("disconnect", function(connection) {
    // Disable the hangup button and enable the call buttons
    $(".hangup-button").prop("disabled", true);
    $(".call-button").prop("disabled", false);

    updateCallStatus("Appel terminé");
});

/* Callback for when Twilio Client receives a new incoming call */
Twilio.Device.on("incoming", function (connection) {
    updateCallStatus("Appel en attente");
    // Set a callback to be executed when the connection is accepted
    connection.on("accept", function() {
        updateCallStatus("Appel en cours");
    });

    $(".answer-button").prop("disabled", false);
    // Set a callback on the answer button and enable it
    $(".answer-button").click(function() {
        connection.accept();
    });
});

/* Call the user from the requests page */
function callUser() {
    updateCallStatus("Appel...");
    console.log("callUSer");
    // Our backend will assume that no params means a call to support_agent
    Twilio.Device.connect();
}

/* End a call */
function hangUp() {
    Twilio.Device.disconnectAll();
}
