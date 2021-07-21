$(document).ready( function(){
    var form = document.querySelector("form");

    var socket = io.connect('http://127.0.0.1:5000');
    var test_button = document.getElementById("test");
    var good_calibration_button = document.getElementById("good_calibration");
    var bad_calibration_button = document.getElementById("bad_calibration");
    var stored_calibration_points = [];
    var formatted_calibration_points = [];

    socket.emit("start_calibration_load");

    socket.on("component_being_calibrated", function(component_information) {
        console.log(component_information)
        var component_type;
        if (component_information[0] == "c"){ component_type = "Chip"; }
        else { component_type = "Plate"; }
        document.getElementById("component").innerHTML = "Component: " + component_type + " (" + component_information[1] + ")";
    });

    form.addEventListener("submit", function(event) {
        var data = new FormData(form); // This stores all the values captured in the form entered by the user
        var index = 0;
        for (const entry of data) {
            stored_calibration_points[index] = parseFloat(entry[1]); // extract the useful information in each entry (only in index 1, index 0 containes the "name" identifier of each HTML input component)
            index++;
        };
        console.log(stored_calibration_points); // DEBUGGING
        document.getElementById("myForm").reset(); // This resets the values of the form after it has been submitted
        var feedback_string = "Calibration Points: ";
        for (var i=0; i<3; i++){
            formatted_calibration_points[i] = [stored_calibration_points[3*i + 0], stored_calibration_points[3*i + 1], stored_calibration_points[3*i + 2]];
            feedback_string = feedback_string + "(" + stored_calibration_points[3*i + 0] + ", " + stored_calibration_points[3*i + 1] + ", " + stored_calibration_points[3*i + 2] + ") ";
        };
        document.getElementById("feedback").innerHTML = feedback_string;
        event.preventDefault();
        test_button.disabled = false; // Enable the test button
    }, false);

    test_button.addEventListener("click", function() {
        console.log(formatted_calibration_points);
        socket.emit("test_calibration", formatted_calibration_points);
        good_calibration_button.disabled = false; // Enable the good_calibration button
        bad_calibration_button.disabled = false; // Enable the bad_calibration button
    });

    good_calibration_button.addEventListener("click", function() {
        socket.emit("good_calibration", formatted_calibration_points);
    });

  })
  