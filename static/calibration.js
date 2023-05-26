var socket = io.connect('http://127.0.0.1:5000');

var stored_calibration_points;
var test_button = document.getElementById("test");
var good_calibration_button = document.getElementById("good_calibration");
var front_left_button = document.getElementById("Move_To_Front_Left");
var back_left_button = document.getElementById("Move_To_Back_Left");
var back_right_button = document.getElementById("Move_To_Back_Right");

var home_page = document.getElementById("home");
var labware_page = document.getElementById("labware");
var protocol_page = document.getElementById("protocol");
var about_page = document.getElementById("about");

socket.emit("give_me_coordinates");
socket.emit("start_calibration");

// Insert box with feedback message here

socket.on("new_coordinates", function(system_update) {
    console.log("new_coordinates")
    document.getElementById("coordinates").innerHTML = "Current Coordinates: " + system_update[0];
});

socket.on("update_front_left", function(update_front_left) {
    console.log("update_front_left")
    document.getElementById("front left").innerHTML = "Current Front Left: " + update_front_left;
});

socket.on("update_back_left", function(update_back_left) {
    console.log("update_back_left")
    document.getElementById("back left").innerHTML = "Current Back Left: " + update_back_left;
});

socket.on("update_back_right", function(update_back_right) {
    console.log("update_back_right")
    document.getElementById("back right").innerHTML = "Current Back Right: " + update_back_right;
});

socket.on("component_being_calibrated", function(component_information) {
    console.log("component_being_calibrated")
    var component_type;
    if (component_information[0] == "c"){ component_type = "Chip"; }
    else { component_type = "Plate"; }
    document.getElementById("component").innerHTML = "Component: " + component_type + " (" + component_information[1] + ")";
});


socket.on("enable_test_calibration", function(calibration_points) {
    console.log("enable_test_calibration")
    console.log(calibration_points)
    stored_calibration_points = calibration_points;
    test_button.disabled = false; // Enable the test button
});

socket.on("enable_move_to_front_left", function() {
    console.log("enable_move_to_front_left")
    front_left_button.disabled = false; // Enable the move to front left button
});

socket.on("enable_move_to_back_left", function() {
    console.log("enable_move_to_back_left")
    back_left_button.disabled = false; // Enable the move to back left button
});

socket.on("enable_move_to_back_right", function() {
    console.log("enable_move_to_back_right")
    back_right_button.disabled = false; // Enable the move to back right button
});

test_button.addEventListener("click", function() {
    console.log("test_button.addEventListener")
    socket.emit("test_calibration", stored_calibration_points);
    good_calibration_button.disabled = false; // Enable the good_calibration button
});


function save_front_left() {
    socket.emit("Save Front Left");
    good_calibration_button.disabled = true; // Disables the good_calibration button until calibration is retested
}

function save_back_left() {
    socket.emit("Save Back Left");
    good_calibration_button.disabled = true; // Disables the good_calibration button until calibration is retested
}

function save_back_right() {
    socket.emit("Save Back Right");
    good_calibration_button.disabled = true; // Disables the good_calibration button until calibration is retested
}

front_left_button.addEventListener("click", function() {
    console.log("front_left_button.addEventListener")
    socket.emit("move_to_front_left");
});

back_left_button.addEventListener("click", function() {
    console.log("back_left_button.addEventListener")
    socket.emit("move_to_back_left");
});

back_right_button.addEventListener("click", function() {
    console.log("back_right_button.addEventListener")
    socket.emit("move_to_back_right");
});

good_calibration_button.addEventListener("click", function() {
    console.log("good_calibration_button.addEventListener")
    console.log(stored_calibration_points)
    socket.emit("stop_calibration");
    socket.emit("good_calibration", stored_calibration_points);
});

home_page.addEventListener("click", function() {
    socket.emit("stop_calibration");
});
labware_page.addEventListener("click", function() {
    socket.emit("stop_calibration");
});
protocol_page.addEventListener("click", function() {
    socket.emit("stop_calibration");
});
about_page.addEventListener("click", function() {
    socket.emit("stop_calibration");
});
