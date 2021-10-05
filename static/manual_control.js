var socket = io.connect('http://127.0.0.1:5000');
var home_button = document.getElementById("back_home");
var load_labware = document.getElementById("load_labware");

//INSTATANEOUS COMMANDS
// Get select components by id
var chip_plate_select = document.getElementById("labware_components");
var component_locations_select = document.getElementById("container_nickname");
var slot_select = document.getElementById("slot_nickname");
var go_button = document.getElementById("go_button");
var show_component_button = document.getElementById("show_component_button");
var previous_labware_selected = "";
var chip_summary_1 = {
    "model": "SZ001",
    "nicknames": ["A0","A1","A2","A3","A4","B0","B1","B2","B3","B4","C0","C1","C2","C3","C4"]
};
var chip_summary_2 = {
    "model": "SZ003",
    "nicknames": ["A0","A1","A2","B0","B1","B2","C0","C1","C2"]
};
var plate_summary_1 = {
    "model": "KW001",
    "nicknames": ["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","B0","B1","B2","B3","B4","B5","B6","B7","B8","B9","C0","C1","C2","C3","C4","C5","C6","C7","C8","C9","D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","E0","E1","E2","E3","E4","E5","E6","E7","E8","E9"]
};

// This is the initialization value but will change as soon as the socket.on method is triggered to receive the actual values of the labware_summary. This assignment is just for testing and documentation purposes
var labware_summary = {
    "chips": [
        chip_summary_1, 
        chip_summary_2
    ],
    "plates": [
        plate_summary_1
    ]
};

populate_component_models(); // This is only needed for testing, when the system is connected to the server this is redundant since it's already done when the socket receives the labware_summary


socket.emit("start_manual_control_window");
socket.emit("give_me_coordinates");
socket.emit("get_labware_summary");

home_button.addEventListener("click", function() {
    socket.emit("stop_manual_control_window");
});

home_button.addEventListener("click", function() {
    socket.emit("stop_manual_control_window");
});

function displaySettings() {
    console.log("We actually hit this function");
    socket.emit("get_syringe_settings");
}

function showPicture() {
    var src = "/static/xbox.jpeg";
    var img = document.getElementById('smallpic')
    img.src = src.replace('90x90','100X100');
    img.style.display="block";
}

function open_lid() {
	console.log("Openning lid");
	socket.emit("open_lid");
}

function screen_info() {
    socket.emit("screen_info");
}

function close_lid() {
    socket.emit("close_lid");
}

function deactivate_all() {
    socket.emit("deactivate_all");
}

function deactivate_lid() {
    socket.emit("deactivate_lid");
}

function deactivate_block() {
    socket.emit("deactivate_block");
}

function set_temperature() {
    let btemp = document.getElementById("btemp");
    let htime = document.getElementById("htime");
    socket.emit("set_temperature", [btemp.value, htime.value]);
}

function set_lid_temperature() {
    let ltemp = document.getElementById("ltemp");
    socket.emit("set_lid_temperature", ltemp.value);
}

function setup_tc_job(data) {
    socket.emit("setup_tc_job", data);
}

function tc_run_job(data) {
    var elements = setup_tc_job(data);
    socket.emit("tc_run_job", elements);
}

function get_block_temp() {
    socket.emit("get_block_temp")
}

function get_lid_temp() {
    socket.emit("get_lid_temp")
}

function home_all_motors() {
	console.log("Home all motors");
	socket.emit("home_all_motors");
}

function home_by_axis(axis){
    socket.emit("hba", axis)
}

function home_X(){
    socket.emit("home_X")
}

function home_Y(){
    socket.emit("home_Y")
}

function home_Z(){
    socket.emit("home_Z")
}

function home_A(){
    socket.emit("home_A")
}

function home_B(){
    socket.emit("home_B")
}

function home_C(){
    socket.emit("home_C")
}

function go_to_deck_slot(slot) {
    socket.emit("go_to_deck_slot", slot);
}

function set_tempdeck_temp() {
    let tdtemp = document.getElementById("tdtemp");
    let thtime = document.getElementById("thtime");
    socket.emit("set_tempdeck_temp", [tdtemp.value, thtime.value]);
}


function deactivate_block() {
    socket.emit("deactivate_block");
}

function deactivate_tempdeck() {
    socket.emit("deactivate_tempdeck")
}

function check_tempdeck_status() {
    socket.emit("check_tempdeck_status")
}

function get_tempdeck_temp() {
    socket.emit("get_tempdeck_temp")
}

function take_picture() {
    socket.emit("take_picture", "Manual Control Pictures")
}

function alert_for_calibration() {
    alert("Please make sure that the OT2 is properly homed before controlling them");
  }

let btemp = 0;
socket.on("get_block_temp", function(temp) {
    console.log(temp)
    btemp = temp;  
    var temp = document.getElementById("blockT")
    temp.innerHTML = btemp;
});

socket.on("get_tempdeck_temp", function(temp) {
    console.log(temp)
    var temp1 = document.getElementById("tdT")
    temp1.innerHTML = temp;
});

socket.on("check_tempdeck_status", function(status) {
    console.log(status)
    var status1 = document.getElementById("tdS")
    status1.innerHTML = status;
});

socket.on("get_lid_temp", function(temp) {
    console.log(temp)
    var temp1 = document.getElementById("lidT")
    temp1.innerHTML = temp;
});

//The socket.on event is placed after the testing call for populate_component_models() to make sure the testing happens before actual data is received and processed (otherwise test data would overwrite actual data)
socket.on("labware_summary", function(labware_summary_received) {
    labware_summary = labware_summary_received;
    // Empty test options added
    reset_chip_plate_options();
    // Populate options for the labware components dropdown list here
    populate_component_models();
});

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

function component_model_onclick() {
    console.log("component_model_onclick called!");
    var option_selected = chip_plate_select.options[ chip_plate_select.selectedIndex ].value;
    console.log(option_selected);
    var current_labware_selected = option_selected;
    var labware_selected_changed = current_labware_selected != previous_labware_selected; // Boolean to see if with the click event on the select component the option selected was changed or not

    // If the value selected changed between click events on the select reset value for the locations dropdown list and disable the GO! button (otherwise it means the user just checked the list but didn't change the option selected)
    if (labware_selected_changed) {
        // Erase all the options inside the dropdown list (select object)
        var length = component_locations_select.options.length;
        // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
        for (var i = length - 1; i >= 0; i--) {
            component_locations_select.remove(i);
        };

        // Add instruction option ()
        var option = document.createElement("option"); // Adding instruction option
        option.text = "- Select a Location -"; // Adding instruction option
        option.value = "default";
        component_locations_select.add(option); // Adding instruction option

        // Set option selected in the component_location dropdown to default option (in case the user selects a component, then a location, and then changes the component. In that case we don't want him to be able to click GO! with a location correpsonding to a different component than the currently selected)
        component_locations_select.value = "default"; // This sets the value of the select to whatever element has its value property set to "default"
    
        // Toggle off GO! button visibility
        go_button.disabled = true;

        previous_labware_selected = current_labware_selected;
    }

    if (option_selected != "default") {
        // If the labware selected changed, fill in the options in the locations dropdown list
        if (labware_selected_changed) {
            // Find the labware component with the model equal to option_selected
            var component_type_selected = option_selected.split("#")[0]
            var index_selected = parseInt(option_selected.split("#")[1][0]) - 1;
            // Extract its locations ("nicknames")
            var locations;
            if (component_type_selected == "Chip ") {
                console.log(labware_summary.chips);
                locations = labware_summary.chips[index_selected].nicknames;
            }
            else {
                console.log(labware_summary.plates);
                locations = labware_summary.plates[index_selected].nicknames;
            }
            // Iterate through that list and add each element in it as an option to component_locations_select
            for (let location of locations) {
                var new_option = document.createElement("option");
                new_option.text = location;
                component_locations_select.add(new_option);
            }
        }
    }

    else {
        // Toggle off GO! button visibility
        go_button.disabled = true;
    }
}

function component_location_onclick() {
    console.log("component_location_onclick called!");
    var option_selected = component_locations_select.options[ component_locations_select.selectedIndex ].value;
    console.log(option_selected);
    if (option_selected != "default") {
        console.log("it's not the default option! Enable GO! button");
        // Toggle on GO! button visibility
        go_button.disabled = false;
    }

    else {
        // Toggle off GO! button visibility
        go_button.disabled = true;
    }
}

function slots_onclick() {
    console.log("slots_onclick called!");
    var option_selected = slot_select.options[ slot_select.selectedIndex ].value;
    console.log(option_selected);
    if (option_selected != "default") {
        console.log("it's not the default option! Enable GO! button");
        // Toggle on GO! button visibility
        show_component_button.disabled = false;
    }

    else {
        // Toggle off GO! button visibility
        show_component_button.disabled = true;
    }
}

function show_component_button_listener(slot){
    socket.emit("get_type_of_labware_by_slot", slot)
}

function go_button_listener() {
    var component = chip_plate_select.value.split("#")[0][0].toLowerCase(); // extracts the lowercase initial of the component type
    var component_index = parseInt(chip_plate_select.value.split("#")[1][0]) - 1; // extracts the index of the labware component
    var component_location = component_locations_select.value; // extracts the location selected within the labware component
    var command = [component, component_index, component_location]; // packs the command in the expected format in web_app.py
    console.log("GO! button pressed :D");
    console.log(command);
    socket.emit("instant_command", command); // Send the command! :D

    var feedback = document.getElementById("user_feedback");
    feedback.innerHTML = `Syringe sent to ${component_location} in ${chip_plate_select.value}`;
}

socket.on("get_syringe_settings", function(givenSetting){
   
    console.log("getting syringe settings");
    var  htmlSetting = document.getElementById("syringe_settings")
    var mybr = "<br />";

    htmlSetting.innerHTML = "Step size S set to: "; 
    htmlSetting.innerHTML += givenSetting["s step"];
    htmlSetting.innerHTML += mybr;

    htmlSetting.innerHTML += "Nanoliters to pick up: ";
    htmlSetting.innerHTML += givenSetting["nL"];
    htmlSetting.innerHTML += mybr;

    htmlSetting.innerHTML += "Step size XYZ set to: "
    htmlSetting.innerHTML += givenSetting["xyz step"]
    htmlSetting.innerHTML += mybr;

    htmlSetting.innerHTML += "Pipette controlling: "
    htmlSetting.innerHTML += givenSetting['pipette']
    htmlSetting.innerHTML += mybr;

    htmlSetting.innerHTML += "X: "
    htmlSetting.innerHTML += givenSetting['x']

    htmlSetting.innerHTML += "  Y: "
    htmlSetting.innerHTML += givenSetting['y']

    htmlSetting.innerHTML += "  Z: "
    htmlSetting.innerHTML += givenSetting['z']
    htmlSetting.innerHTML += mybr;

    htmlSetting.innerHTML += "  SC_B: "
    htmlSetting.innerHTML += givenSetting['b']
    htmlSetting.innerHTML += "  SC_C: "
    htmlSetting.innerHTML += givenSetting['c']  
});