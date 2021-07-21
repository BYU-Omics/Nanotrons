var socket = io.connect('http://127.0.0.1:5000');

var stored_calibration_points;
var home_button = document.getElementById("back_home");
var test_button = document.getElementById("test");
var good_calibration_button = document.getElementById("good_calibration");
var bad_calibration_button = document.getElementById("bad_calibration");
var calibration_feedback = document.getElementById("feedback_calibration_points");

// socket.emit("start_manual_control_window")
// console.log("start_manual_control_window")
socket.emit("give_me_coordinates");
socket.emit("start_calibration");

// Insert box with feedback message here

socket.on("new_coordinates", function(system_update) {
    console.log("new_coordinates")
    document.getElementById("coordinates").innerHTML = "Current Coordinates: " + system_update[0];
});

socket.on("component_being_calibrated", function(component_information) {
    console.log("component_being_calibrated")
    var component_type;
    if (component_information[0] == "c"){ component_type = "Chip"; }
    else { component_type = "Plate"; }
    document.getElementById("component").innerHTML = "Component: " + component_type + " (" + component_information[1] + ")";
});

socket.on("feedback_calibration_point", function(new_position) {
    console.log("feedback_calibration_point")
    // feedback_received++;
    console.log("new_position:", new_position);
    var node = document.createElement('li'); // Create a list element
    node.appendChild(document.createTextNode("(" + new_position[0] + ", " + new_position[1] + ", " + new_position[2] + ")")); // (feedback_received + ". " + new_position)); // Append a text node to the list element node
    calibration_feedback.appendChild(node); // Add the node to the feedback list
});

socket.on("stored_calibration_points", function(calibration_points) {
    console.log("stored_calibration_points")
    test_button.disabled = false; // Enable the test button
    console.log(calibration_points)
    stored_calibration_points = calibration_points;
});

test_button.addEventListener("click", function() {
    console.log("test_button.addEventListener")
    socket.emit("test_calibration", stored_calibration_points);
    good_calibration_button.disabled = false; // Enable the good_calibration button
    bad_calibration_button.disabled = false; // Enable the bad_calibration button
});

home_button.addEventListener("click", function() {
    console.log("home_button.addEventListener")
    socket.emit("stop_calibration");
});

function screen_info() {
    socket.emit("screen_info");
}

function up_step_size() {
    socket.emit("up_step_size");
}

function down_step_size() {
    socket.emit("down_step_size");
}

function stop_manual_control_window() {
    socket.emit("stop_manual_control_window");
}

function go_to_deck_slot(slot) {
    socket.emit("go_to_deck_slot", slot);
}

good_calibration_button.addEventListener("click", function() {
    console.log("good_calibration_button.addEventListener")
    console.log(stored_calibration_points);
    socket.emit("good_calibration", stored_calibration_points);
});
