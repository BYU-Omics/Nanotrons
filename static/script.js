var socket = io.connect('http://127.0.0.1:5000');

var run_protocol_button = document.getElementById("run_protocol");
var protocolOptions = document.getElementById("protocols"); // Dropdown list that shows the available models
var calibrationOptions = document.getElementById("calibration"); // Dropdown list that shows the available models
var syringeOptions = document.getElementById("syringe"); // Dropdown list that shows the available models


var display_protocol_button = document.getElementById("display_protocol");
var display_calibration_button = document.getElementById("display_calibration");
var display_syringe_button = document.getElementById("display_syringe");

var pause_button_protocol = document.getElementById("pause_protocol");
var stop_button_protocol = document.getElementById("stop_protocol")
var continue_button_protocol = document.getElementById("continue_protocol")

var stopLoad_button = document.getElementById("stop_load");
var hardStop_button = document.getElementById("hard_stop");
var protocol_name = document.getElementById("protocol_name");
var script_description = document.getElementById("script_description");
var protocol_description = document.getElementById("protocol_description");
var gradientTime = document.getElementById("gradientTime");
var SPEtime = document.getElementById("SPEtime");

var contents = ""
var protocols = {}
var calibrations = {}
var syringes = {}
var script_to_display = "error" // save as error until over written
var protocol_to_display = "error"
var calibration_to_display = "error"
var syringe_to_display = "error"

var json_data = "" // will hold the json data from the script
var python_data = ""

// asks python to send the list of scripts

socket.emit("get_available_protocols")
socket.emit("get_available_calibrations")
socket.emit("get_available_syringes")
// socket.emit("give_me_protocol_python")

// listens for the list of available scripts
socket.on('protocols_available', function(received_protocols) {
    protocols = received_protocols; // save list in scripts variable
    console.log("protocol received")
    fill_protocol_drop_down() // add the options to the list
}); 

// listens for the list of available scripts
socket.on('calibrations_available', function(received_calibrations) {
    calibrations = received_calibrations; // save list in scripts variable
    console.log("calibrations received")
    fill_calibrations_drop_down() // add the options to the list
}); 

// listens for the list of available scripts
socket.on('syringes_available', function(received_syringes) {
    syringes = received_syringes; // save list in scripts variable
    console.log("syringes received")
    fill_syringes_drop_down() // add the options to the list
}); 

socket.on('display_contents', function(file_contents) {
    python_file_contents = file_contents
});


// fills drop down list with the availble scripts
function fill_protocol_drop_down(){
    // Erase all the options inside the dropdown list (select object)
    var length = protocolOptions.options.length;
    // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
    for (var i = length - 1; i >= 0; i--) {
        protocolOptions.remove(i);
    };
    
    // Add instruction option ()
    var python_option = document.createElement("option"); // Adding instruction option
    python_option.text = "- Select a Protocol -"; // Adding instruction option
    protocolOptions.add(python_option); // Adding instruction option

    // Loop that adds the options to the options_list
    for (var i = 0; i < protocols.length; i++){  
        var python_option = document.createElement("option");
        python_option.text = protocols[i];
        protocolOptions.add(python_option);
    }

}

// fills drop down list with the availble scripts
function fill_calibrations_drop_down(){
    // Erase all the options inside the dropdown list (select object)
    var length = calibrationOptions.options.length;
    // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
    for (var i = length - 1; i >= 0; i--) {
        calibrationOptions.remove(i);
    };
    
    // Add instruction option ()
    var python_option = document.createElement("option"); // Adding instruction option
    python_option.text = "- Select a calibration -"; // Adding instruction option
    calibrationOptions.add(python_option); // Adding instruction option

    // Loop that adds the options to the options_list
    for (var i = 0; i < calibrations.length; i++){  
        var python_option = document.createElement("option");
        python_option.text = calibrations[i];
        calibrationOptions.add(python_option);
    }
}

// fills drop down list with the availble scripts
function fill_syringes_drop_down(){
    // Erase all the options inside the dropdown list (select object)
    var length = syringeOptions.options.length;
    // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
    for (var i = length - 1; i >= 0; i--) {
        syringeOptions.remove(i);
    };
    
    // Add instruction option ()
    var python_option = document.createElement("option"); // Adding instruction option
    python_option.text = "- Select a syringe -"; // Adding instruction option
    syringeOptions.add(python_option); // Adding instruction option

    // Loop that adds the options to the options_list
    for (var i = 0; i < syringes.length; i++){  
        var python_option = document.createElement("option");
        python_option.text = syringes[i];
        syringeOptions.add(python_option);
    }
}

// this runs each time you select an option from the script list
function option_select_protocol(){
    // This either blocks or unblocks the submit button
    var selected_protocol = protocolOptions.options[ protocolOptions.selectedIndex ].value;
    protocol_to_display = selected_protocol; // set variable to the selected value
    console.log(selected_protocol);
    socket.emit("set_protocol_filename", protocol_to_display)
    if ( selected_protocol != "- Select a Protocol -" ) { // if you select something from the list
        display_protocol_button.disabled = false; // enable the button
    }
    else { // if you select the instructions from the list
        display_protocol_button.disabled = true; // disable button
    }
}

// this runs each time you select an option from the script list
function option_select_labware_calibration(){
    // This either blocks or unblocks the submit button
    var selected_calibration = calibrationOptions.options[ calibrationOptions.selectedIndex ].value;
    calibration_to_display = selected_calibration; // set variable to the selected value
    console.log(selected_calibration);
    socket.emit("set_labware_calibration", selected_calibration)
    if ( selected_calibration != "- Select a calibration -" ) { // if you select something from the list
        display_calibration_button.disabled = false; // enable the button
    }
    else { // if you select the instructions from the list
        display_calibration_button.disabled = true; // disable button
    }
}

// this runs each time you select an option from the script list
function option_select_syringe(){
    // This either blocks or unblocks the submit button
    var selected_syringe = syringeOptions.options[ syringeOptions.selectedIndex ].value;
    syringe_to_display = selected_syringe; // set variable to the selected value
    console.log(selected_syringe);
    socket.emit("set_labware_syringe", selected_syringe)
    if ( selected_syringe != "- Select a syringe -" ) { // if you select something from the list
        display_syringe_button.disabled = false; // enable the button
    }
    else { // if you select the instructions from the list
        display_syringe_button.disabled = true; // disable button
    }
}

// this runs when you click the display script button
display_protocol_button.addEventListener("click", function() {
    // clear_protocol_Table() // clear out the old table data
    console.log("clearing table")
});


// listens for the json data
socket.on('protocol_python_data', function(python_lines_list) {
    console.log("protocols received")
    python_data = python_lines_list; // save list in scripts variable
    var content = document.getElementById("file_contents")
    
    text_area_left = '<textarea id="w3review" name="w3review" rows="4" cols="50">'
    text_area_right = '</textarea>'
    text = "<br>" + text_area_left
    for (let i = 36; i < python_data.length; i++) {
        console.log(python_data[i][0])
        if (python_data[i][0] == '#') {
            text +=  python_data[i] ;
        } else {
            
            text += python_data[i] ;
        }
    }
    content.innerHTML = text + text_area_right + "<br>"
    // console.log(text)
    
    
    // make_and_display_protocol_table()
});  

function display_contents() {
    socket.emit("display_contents")
}


// fills in the table with script commands
function make_and_display_protocol_table(){
    console.log(python_data)
    var obj1 = PY.parse(python_data)
    var obj = JSON.parse(python_data); // parse the JSON string into JSON obj
    console.log("Name " + obj.name);

    protocol_name.innerHTML = obj.name;               // These 6 lines get name, description, MStime, LCtime, GradientTime, and SPEtime
    protocol_description.innerHTML = obj.description; // from the json data
    gradientTime.innerHTML = obj.gradientTime;
    SPEtime.innerHTML = obj.SPEtime;

    for(var i = 0; i < obj.commands.length; i++) { // loop for each command
        var command = obj.commands[i]; 
    
        var commmandType = command.type;
        var parameters = command.parameters;
        addRow(commmandType, parameters); // add row to table with the command and parameters
    }
}

run_protocol_button.addEventListener("click", function() {
    socket.emit("run_protocol", protocol_to_display);
});

// the pause button in HTML. Calls the pause batch function
pause_button_protocol.addEventListener("click", function() {
    socket.emit("pause_protocol");
});

stop_button_protocol.addEventListener("click", function() {
    socket.emit("stop_protocol")
});

continue_button_protocol.addEventListener("click", function() {
    socket.emit("continue_protocol")
});

// the stop load button in HTML. Calls the stop_load function
stopLoad_button.addEventListener("click", function() {
    socket.emit("stop_load");
});

// the hard stop button in HTML. Calls the hardstop function
hardStop_button.addEventListener("click", function() {
    socket.emit("hard_stop");
});

// allows you to upload a new script that you can display
function uploadScript() {
    var socket = io.connect('http://127.0.0.1:5000');
    console.log("upload script")
}

// adds a row to the table with the given parameters
function addRow(command, parameters) {
    var myName = document.getElementById("name");
    var age = document.getElementById("age");
    var table = document.getElementById("myTableData");
 
    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);
 
    row.insertCell(0).innerHTML= '<input type="button" value = "Delete" onClick="Javacsript:deleteRow(this)">';
    row.insertCell(1).innerHTML= command;
    row.insertCell(2).innerHTML= parameters;
 
}

function clear_script_Table(){
    var table = document.getElementById("myScriptTableData");
    console.log("Table size:" + table.tBodies[0].rows.length);
    var length = table.tBodies[0].rows.length;
    for(var i = 0; i < length - 1; i++) { // loop for row in table
        table.deleteRow_script(length - 1 - i); // delete each row from back to front
    }
}

function clear_protocol_Table(){
    var table = document.getElementById("myProtocolTableData");
    console.log("Table size:" + table.tBodies[0].rows.length);
    var length = table.tBodies[0].rows.length;
    for(var i = 0; i < length - 1; i++) { // loop for row in table
        table.deleteRow_protocol(length - 1 - i); // delete each row from back to front
    }
}

function deleteRow_script(obj) {
      
    var index = obj.parentNode.parentNode.rowIndex;
    var table = document.getElementById("myScriptTableData");
    table.deleteRow(index);
}

function deleteRow_protocol(obj) {
      
    var index = obj.parentNode.parentNode.rowIndex;
    var table = document.getElementById("myProtocolTableData");
    table.deleteRow(index);
}

function addTable() {
      
    var myTableDiv = document.getElementById("myDynamicTable");
      
    table = document.createTextNode("Help");
    myTableDiv.appendChild(table);
}
 
function load() {
    console.log("Page load finished");
}
