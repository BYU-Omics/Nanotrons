$(document).ready( function(){

    // Set up the socket connection 
    var socket = io.connect('http://127.0.0.1:5000'); 

    // This is supposed to be received through a socket event, but this is for testing purposes
    var models = {};

    var selected;

    socket.emit("get_labware_models");

    socket.on('models_available', function(received_models) {
        models = received_models;
    });    

    // Obtain input objects from the HTML code
    var selectedChip = document.getElementById("ContainerC"); // Radio button corresponding to the Chip option
    var selectedPlate = document.getElementById("ContainerP"); // Radio button corresponding to the Plate option
    var modelOptions = document.getElementById("models"); // Dropdown list that shows the available models
    var calibrateButton = document.getElementById("calibrate"); // Button that triggers a calibration

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

    }
    // Event handler in case the radio button for "Chip" is clicked
    selectedChip.onclick = function() {
        selected = "c" 
        fill_model_options("chips");
    }
    
    // Event handler in case the radio button for "Plate" is clicked
    selectedPlate.onclick = function() {
        selected = "p"
        fill_model_options("plates");
    }

    // This method checks the values of the model select object when it's clicked upon
    modelOptions.onclick = function() {

        // This returns the value of the selection
        var selected_model = modelOptions.options[ modelOptions.selectedIndex ].value;
        console.log(selected_model)
        if ( (selected_model != "- Select a Model -") && (selected_model != "- Select Chip or Reagent Plate -") ) {
            calibrateButton.disabled = false;
            var command = [];
            command[0] = (selected)
            command[1] = selected_model
            console.log(command);
            socket.emit("calibration_parameters", command);

        }
    }
})