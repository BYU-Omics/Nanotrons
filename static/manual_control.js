var socket = io.connect('http://127.0.0.1:5000/');
var home_page = document.getElementById("DrpDwnMn0-5s30label");
var labware_page = document.getElementById("DrpDwnMn0-5s32label");
var protocol_page = document.getElementById("DrpDwnMn0-5s33label");
var about_page = document.getElementById("DrpDwnMn0-5s34label");
var load_labware = document.getElementById("load_labware");

//INSTATANEOUS COMMANDS
// Get select components by id
var model_select = document.getElementById("labware_components");
var component_locations_select = document.getElementById("container_nickname");
var slot_select = document.getElementById("slot_nickname");
var go_button = document.getElementById("go_button");
var show_component_button = document.getElementById("show_component_button");
var previous_labware_selected = "";
var newArray = []; 


//The socket.on event is placed after the testing call for populate_component_models() to make sure the testing happens before actual data is received and processed (otherwise test data would overwrite actual data)
socket.on("labware_summary", function(labware_summary_received) {
    console.log("here is the labware summary" + labware_summary_received)
    labware_summary = labware_summary_received;
    // Empty test options added
    reset_model_options();
    // Populate options for the labware components dropdown list here
    populate_component_models();
});

socket.emit("start_manual_control_window");
socket.emit("give_me_coordinates");

socket.emit("give_me_current_labware");
socket.emit("get_labware_summary");


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

function open_close_lid() {
    socket.emit("open_close_lid");
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

socket.on("rename_deck_slot", function(slotInt) {
    var someButton = document.getElementById(slotInt);
    // someButton.innerHTML("Hello World");
    someButton.innerText("Hello world");
});

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
    console.log("Take picture")
    socket.emit("take_picture", "ManualCtrlPics")
}

function alert_for_calibration() {
    alert("Please make sure that the OT2 is properly homed before controlling them");
}

function toggle_focus() {
    socket.emit("toggle_focus");
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

function reset_model_options() {
    // Erase all the options inside the dropdown list (select object)
    var length = model_select.options.length;
    // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
    for (var i = length - 1; i >= 0; i--) {
        model_select.remove(i);
    };
    // Add the default option
    var new_option = document.createElement("option");
    new_option.text = "- Select a Labware Component -";
    model_select.add(new_option);
}

function populate_component_models() {
    index = 1;
    for (let model_summary of labware_summary.models) {
        var new_option = document.createElement("option");
        new_option.text = `Model #${index} - ` + model_summary["model"];
        model_select.add(new_option);
        index++;
    }
}

function component_model_onclick() {
    console.log("component_model_onclick called!");
    var option_selected = model_select.options[ model_select.selectedIndex ].value;
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
            var index_selected = parseInt(option_selected.split("#")[1][0]) - 1;
            // Extract its locations ("nicknames")
            var locations;
                locations = labware_summary.models[index_selected].nicknames;
                console.log("these are the locations " + locations)

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
    var component = model_select.value.split("#")[0][0].toLowerCase(); // extracts the lowercase initial of the component type
    var component_index = parseInt(model_select.value.split("#")[1][0]) - 1; // extracts the index of the labware component
    var component_location = component_locations_select.value; // extracts the location selected within the labware component
    var command = [component, component_index, component_location]; // packs the command in the expected format in web_app.py
    console.log("GO! button pressed :D");
    console.log(command);
    socket.emit("instant_command", command); // Send the command! :D

    var feedback = document.getElementById("user_feedback");
    feedback.innerHTML = `Syringe sent to ${component_location} in ${model_select.value}`;
}

socket.on("get_syringe_settings", function(givenSetting){
    console.log("getting syringe settings");
    var  htmlSetting = document.getElementById("syringe_settings")
    var mybr = "<br />";

    htmlSetting.innerHTML = "Step size:  S: "; 
    htmlSetting.innerHTML += givenSetting["s step"];

    htmlSetting.innerHTML += "   XYZ: "
    htmlSetting.innerHTML += givenSetting["xyz step"]
    htmlSetting.innerHTML += mybr;

    htmlSetting.innerHTML += "Nanoliters to pick up: ";
    htmlSetting.innerHTML += givenSetting["nL"];
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

    htmlSetting.innerHTML += "  SC_B: "
    htmlSetting.innerHTML += givenSetting['b']
    
    htmlSetting.innerHTML += "  SC_C: "
    htmlSetting.innerHTML += givenSetting['c']  

});

home_page.addEventListener("click", function() {
    socket.emit("stop_manual_control_window");
});
labware_page.addEventListener("click", function() {
    socket.emit("stop_manual_control_window");
});
protocol_page.addEventListener("click", function() {
    socket.emit("stop_manual_control_window");
});
