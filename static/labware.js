var form = document.querySelector("form");

var socket = io.connect('http://127.0.0.1:5000');

var chip_plate_select = document.getElementById("labware_components");
var component_locations_select = document.getElementById("container_nickname");
var calibrated_chips = document.getElementById("calibrated_chips");
var calibrated_plates = document.getElementById("calibrated_plates");
var delete_button = document.getElementById("delete_button");
var delete_form = document.getElementById("delete_form");
var newArray = [];

socket.emit("give_me_current_labware");
socket.emit("get_labware_summary");


delete_button.addEventListener("click", function(){
    console.log("remove_component_onclick called!");
    socket.emit("remove_component_onclick", newArray); 
});

socket.on("here_current_labware", function(labware_dict) {
    console.log(labware_dict);

    // Update the list of chips
    for (var i = 0; i < labware_dict["chips"].length; i++){
        var node = document.createElement('li'); // Create a list element
        node.appendChild(document.createTextNode(labware_dict["chips"][i])); // Append a text node to the list element node
        calibrated_chips.appendChild(node); // Add the node to the labware list
    }

    // Update the list of plates
    for (var i = 0; i < labware_dict["plates"].length; i++){
        var node = document.createElement('li'); // Create a list element
        node.appendChild(document.createTextNode(labware_dict["plates"][i])); // Append a text node to the list element node
        calibrated_plates.appendChild(node); // Add the node to the labware list
    }
});

socket.on("labware_summary", function(labware_summary_received) {
    labware_summary = labware_summary_received;
    // Empty test options added
    reset_chip_plate_options();
    // Populate options for the labware components dropdown list here
    populate_component_models();
});

form.addEventListener("submit", function(event) {
    var data = new FormData(form); // This stores all the values captured in the form entered by the user
    var command = []; // This array will hold the values to be sent to the python code
    var index = 0;
    for (const entry of data) {
	command[index] = entry[1]; // extract the useful information in each entry (only in index 1, index 0 containes the "name" identifier of each HTML input component)
		if (index == 1) {
			command[index]--; // The second element is the index of the component to be removed and the user list starts at 1, so this corrects for that difference (system starts at index 0)
		}
		index++;
    };
    console.log(command); // DEBUGGING
    alert("continue?");
    socket.emit("delete_labware", command);
    document.getElementById("myForm").reset(); // This resets the values of the form after it has been submitted
    document.getElementById("feedback").innerHTML = "Component: "+ command[0] + " # " + command[1];
    event.preventDefault();
  }, false);

  function reset_chip_plate_options() {
    // Erase all the options inside the dropdown list (select object)
    var length = chip_plate_select.options.length;
    // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
    for (var i = length - 1; i >= 0; i--) {
        chip_plate_select.remove(i);
    };
    // Add the default option
    var new_option = document.createElement("option");
    new_option.text = "- Select a Labware Component -";
    chip_plate_select.add(new_option);
}

function populate_component_models() {
    var index = 1;
    for (let chip_summary of labware_summary.chips) {
        var new_option = document.createElement("option");
        new_option.text = `Chip #${index} - ` + chip_summary["model"];
        chip_plate_select.add(new_option);
        index++;
    }
    index = 1;
    for (let plate_summary of labware_summary.plates) {
        var new_option = document.createElement("option");
        new_option.text = `Plate #${index} - ` + plate_summary["model"];
        chip_plate_select.add(new_option);
        index++;
    }
}

var labware_summary = {
    "chips": [
        chip_summary_1, 
        chip_summary_2
    ],
    "plates": [
        plate_summary_1
    ]
};

function component_model_onclick() {
    console.log("component_model_onclick called!");
    var option_selected = chip_plate_select.options[ chip_plate_select.selectedIndex ].value;
    console.log(option_selected);
    var current_labware_selected = option_selected;
    var labware_selected_changed = current_labware_selected != previous_labware_selected; // Boolean to see if with the click event on the select component the option selected was changed or not

    if (option_selected != "default") {
        // If the labware selected changed, fill in the options in the locations dropdown list
        if (labware_selected_changed) {
            // Find the labware component with the model equal to option_selected
            var component_type_selected = option_selected.split("#")[0]
            var index_selected = parseInt(option_selected.split("#")[1][0]) - 1;
            console.log("here is this " + index_selected)
    
            if (component_type_selected == "Chip ") {
                newArray[0] = 'c';
                newArray[1] = index_selected;
            }
            else {
                newArray[0] = 'p';
                newArray[1] = index_selected;
            }
        }
    }
}