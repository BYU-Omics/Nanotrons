$(document).ready( function(){
    // Allows for dynamic content display (without needing to reload the website)
    var form = document.querySelector("form");
  
    // Set up the socket connection 
    var socket = io.connect('http://127.0.0.1:5000');

    // This is supposed to be received through a socket event, but this is for testing purposes
    var models = {};

    socket.emit("get_labware_models");

    socket.on('models_available', function(received_models) {
        models = received_models;
    });    

    // Obtain input objects from the HTML code
    var selectedChip = document.getElementById("ContainerC"); // Radio button corresponding to the Chip option
    var selectedPlate = document.getElementById("ContainerP"); // Radio button corresponding to the Plate option
    var modelOptions = document.getElementById("models"); // Dropdown list that shows the available models
    var calibrateButton = document.getElementById("calibrate"); // Button that triggers a calibration
    var loadCalibrationButton = document.getElementById("load_calibration"); // Button that directs to loading a calibration
    var uploadNewModel = document.getElementById("upload_model");
    var loadButton = document.getElementById("load_empty_button");
    
    loadButton.load_stuff = function(){
        var data = new FormData(form); // This stores all the values captured in the form entered by the user
        console.log("Form data: ", data)
        var command = []; // This array will hold the values to be sent to the python code
        var index = 0;
        for (const entry of data) {
            command[index] = entry[1]; // extract the useful information in each entry (only in index 1, index 0 containes the "name" identifier of each HTML input component)
            index++;
        };

        console.log(command); // example output: ["c", "SZ002"]
        // Send the data captured from the form to the Python code through the socket
        socket.emit("calibration_parameters", command);
        document.getElementById("myForm").reset(); // This resets the values of the form after it has been submitted
    }

    function fill_model_options(chip_or_plate) {
        // Erase all the options inside the dropdown list (select object)
        var length = modelOptions.options.length;
        // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
        for (var i = length - 1; i >= 0; i--) {
            modelOptions.remove(i);
        };

        // Add instruction option ()
        var option = document.createElement("option"); // Adding instruction option
        option.text = "- Select a Model -"; // Adding instruction option
        modelOptions.add(option); // Adding instruction option

        // Add options of models for chip or plate depending on the argument of this function

        // Container for the options
        var options_list;
        if (chip_or_plate == "chips"){
            options_list = models["chips"];
        }
        else {
            options_list = models["plates"];
        }
        // Loop that adds the options to the options_list
        for (var i = 0; i < options_list.length; i++){  
            var option = document.createElement("option");
            option.text = options_list[i];
            modelOptions.add(option);
        }

        // This either blocks or unblocks the submit button
        var selected_model = modelOptions.options[ modelOptions.selectedIndex ].value;
        // console.log(selected_model);
        if ( selected_model != "- Select a Model -" ) {
            calibrateButton.disabled = false;
            loadCalibrationButton.disabled = false;
        }
        else {
            calibrateButton.disabled = true;
            loadCalibrationButton.disabled = true;
        }
    }

    // Event handler in case the radio button for "Chip" is clicked
    selectedChip.onclick = function() {
        uploadNewModel.disabled = false; // Activate the upload new model button
        fill_model_options("chips");
    }
    
    // Event handler in case the radio button for "Plate" is clicked
    selectedPlate.onclick = function() {
        uploadNewModel.disabled = false; // Activate the upload new model button
        fill_model_options("plates");
    }

    // This method checks the values of the model select object when it's clicked upon
    modelOptions.onclick = function() {

        // This returns the value of the selection
        var selected_model = modelOptions.options[ modelOptions.selectedIndex ].value;
        console.log(selected_model)
        if ( (selected_model != "- Select a Model -") && (selected_model != "- Select Chip or Reagent Plate -") ) {
            calibrateButton.disabled = false;
            loadCalibrationButton.disabled = false;
            loadButton.disabled = false;
        }
        else {
            calibrateButton.disabled = true;
            loadCalibrationButton.disabled = true;
            loadButton.disabled = true;
        }
    }

    // Event listener for the form object. Gets activated when the submit button is pressed and captures the values entered
    form.addEventListener("submit", function(event) {
        var data = new FormData(form); // This stores all the values captured in the form entered by the user
        console.log("Form data: ", data)
        var command = []; // This array will hold the values to be sent to the python code
        var index = 0;
        for (const entry of data) {
            command[index] = entry[1]; // extract the useful information in each entry (only in index 1, index 0 containes the "name" identifier of each HTML input component)
            index++;
        };

        console.log(command); // example output: ["c", "SZ002"]
        // Send the data captured from the form to the Python code through the socket
        socket.emit("calibration_parameters", command);
        document.getElementById("myForm").reset(); // This resets the values of the form after it has been submitted
        event.preventDefault(); // don't know if this is needed
    });

})