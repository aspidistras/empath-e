// Store some selectors for elements we'll reuse
var callStatus = $("#call-status");
var answerButton = $(".answer-button");
var callButton = $(".call-button");
var hangUpButton = $(".hangup-button");

/* Helper function to update the call status bar */
function updateCallStatus(status) {
    callStatus.attr('placeholder', status);
}

/* Get a Twilio Client token with an AJAX request */
$(document).ready(function() {
    $.get("/contact/token", {forPage: window.location.pathname}, function(data) {
        // Set up the Twilio Client Device with the token
        Twilio.Device.setup(data.token);
    });
});

/* Callback to let us know Twilio Client is ready */
Twilio.Device.ready(function (device) {
    updateCallStatus("Ready");
});

/* Report any errors to the call status display */
Twilio.Device.error(function (error) {
    updateCallStatus("ERROR: " + error.message);
});

/* Callback for when Twilio Client initiates a new connection */
Twilio.Device.connect(function (connection) {
    // Enable the hang up button and disable the call buttons
    hangUpButton.prop("disabled", false);
    callButton.prop("disabled", true);
    answerButton.prop("disabled", true);

    updateCallStatus("Appel en cours");
});

/* Callback for when a call ends */
Twilio.Device.disconnect(function(connection) {
    // Disable the hangup button and enable the call buttons
    hangUpButton.prop("disabled", true);
    callButton.prop("disabled", false);

    updateCallStatus("Appel terminé");
});

/* Callback for when Twilio Client receives a new incoming call */
Twilio.Device.incoming(function(connection) {
    updateCallStatus("Appel en attente");

    // Set a callback to be executed when the connection is accepted
    connection.accept(function() {
        updateCallStatus("Appel en cours");
    });

    // Set a callback on the answer button and enable it
    answerButton.click(function() {
        connection.accept();
    });
    answerButton.prop("disabled", false);
});

/* Call the user from the requests page */
function callUser() {
    updateCallStatus("Appel...");

    // Our backend will assume that no params means a call to support_agent
    Twilio.Device.connect();
}

/* End a call */
function hangUp() {
    Twilio.Device.disconnectAll();
}
