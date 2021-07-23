var socket = io.connect('http://127.0.0.1:5000');

var run_protocol_button = document.getElementById("run_protocol");
var protocolOptions = document.getElementById("protocols"); // Dropdown list that shows the available models
var calibrationOptions = document.getElementById("calibration"); // Dropdown list that shows the available models

var display_protocol_button = document.getElementById("display_protocol");
var display_calibration_button = document.getElementById("display_calibration");

var pause_button_protocol = document.getElementById("pause_protocol");
var stop_button_protocol = document.getElementById("stop_protocol")

var stopLoad_button = document.getElementById("stop_load");
var hardStop_button = document.getElementById("hard_stop");
var protocol_name = document.getElementById("protocol_name");
var script_description = document.getElementById("script_description");
var protocol_description = document.getElementById("protocol_description");
var gradientTime = document.getElementById("gradientTime");
var SPEtime = document.getElementById("SPEtime");

var protocols = {}
var calibrations = {}
var script_to_display = "error" // save as error until over written
var protocol_to_display = "error"
var calibration_to_display = "error"
var json_data = "" // will hold the json data from the script
var python_data = ""

// asks python to send the list of scripts

<<<<<<< HEAD
socket.emit("get_available_scripts");
=======
>>>>>>> newrepo
socket.emit("get_available_protocols")
socket.emit("get_available_calibrations")

// listens for the list of available scripts
<<<<<<< HEAD
socket.on('scripts_available', function(received_scripts) {
    scripts = received_scripts; // save list in scripts variable
    console.log("scripts recieved")
    fill_script_drop_down() // add the options to the list
});   

// listens for the list of available scripts
=======
>>>>>>> newrepo
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

// fills drop down list with the availble scripts
<<<<<<< HEAD
function fill_script_drop_down(){
    // Erase all the options inside the dropdown list (select object)
    var length = scriptOptions.options.length;
    // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
    for (var i = length - 1; i >= 0; i--) {
        scriptOptions.remove(i);
    };
    
    // Add instruction option ()
    var script_option = document.createElement("option"); // Adding instruction option
    script_option.text = "- Select a Script -"; // Adding instruction option
    scriptOptions.add(script_option); // Adding instruction option

    // Loop that adds the options to the options_list
    for (var i = 0; i < scripts.length; i++){  
        var script_option = document.createElement("option");
        script_option.text = scripts[i];
        scriptOptions.add(script_option);
    }

}

// fills drop down list with the availble scripts
=======
>>>>>>> newrepo
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

// this runs each time you select an option from the script list
<<<<<<< HEAD
function option_select_script(){
    // This either blocks or unblocks the submit button
    var selected_script = scriptOptions.options[ scriptOptions.selectedIndex ].value;
    script_to_display = selected_script; // set variable to the selected value
    console.log(selected_script);
    if ( selected_script != "- Select a Script -" ) { // if you select something from the list
        display_script_button.disabled = false; // enable the button
    }
    else { // if you select the instructions from the list
        display_script_button.disabled = true; // disable button
    }
}

// this runs each time you select an option from the script list
=======
>>>>>>> newrepo
function option_select_protocol(){
    // This either blocks or unblocks the submit button
    var selected_protocol = protocolOptions.options[ protocolOptions.selectedIndex ].value;
    protocol_to_display = selected_protocol; // set variable to the selected value
    console.log(selected_protocol);
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
<<<<<<< HEAD
// this runs when you click the display script button
display_script_button.addEventListener("click", function() {
    clear_script_Table() // clear out the old table data
    console.log("clearing table")
    socket.emit("give_me_script_json", script_to_display);
});
=======
>>>>>>> newrepo

// this runs when you click the display script button
display_protocol_button.addEventListener("click", function() {
    clear_protocol_Table() // clear out the old table data
    console.log("clearing table")
    socket.emit("give_me_protocol_python", protocol_to_display);
});


// listens for the json data
socket.on('protocol_python_data', function(python_string) {
    python_data = python_string; // save list in scripts variable
    console.log("protocols received")
    make_and_display_protocol_table()
});  

<<<<<<< HEAD
// listens for the json data
socket.on('script_json_data', function(json_string) {
    json_data = json_string; // save list in scripts variable
    console.log("scripts recieved")
    make_and_display_script_table()
});  

// fills in the table with script commands
function make_and_display_script_table(){
    console.log(json_data)
    var obj = JSON.parse(json_data); // parse the JSON string into JSON obj
    console.log("Name " + obj.name);

    script_name.innerHTML = obj.name;               // These 6 lines get name, description, MStime, LCtime, GradientTime, and SPEtime
    script_description.innerHTML = obj.description; // from the json data
    MStime.innerHTML = obj.MStime;                  // The command vector is parced and displayed in a table in the for loop below
    LCtime.innerHTML = obj.LCtime;
    gradientTime.innerHTML = obj.gradientTime;
    SPEtime.innerHTML = obj.SPEtime;

    for(var i = 0; i < obj.commands.length; i++) { // loop for each command
        var command = obj.commands[i]; 
    
        var commmandType = command.type;
        var parameters = command.parameters;
        addRow(commmandType, parameters); // add row to table with the command and parameters
    }
}

=======
>>>>>>> newrepo
// fills in the table with script commands
function make_and_display_protocol_table(){
    console.log(python_data)
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

<<<<<<< HEAD
// the play button in HTML. Calls the run batch function
run_script_button.addEventListener("click", function() {
    socket.emit("run_script");
});

=======
>>>>>>> newrepo
run_protocol_button.addEventListener("click", function() {
    socket.emit("run_protocol", protocol_to_display);
});

// the pause button in HTML. Calls the pause batch function
<<<<<<< HEAD
pause_button_script.addEventListener("click", function() {
    socket.emit("pause_batch");
});

// the pause button in HTML. Calls the pause batch function
pause_button_script.addEventListener("click", function() {
    socket.emit("pause_protocol");
=======
pause_button_protocol.addEventListener("click", function() {
    socket.emit("pause_protocol");
});

stop_button_protocol.addEventListener("click", function() {
    socket.emit("stop_protocol")
>>>>>>> newrepo
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
<<<<<<< HEAD

    console.log("upload script")

=======
    console.log("upload script")
>>>>>>> newrepo
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
      
    var table = document.createElement('TABLE');
    table.border='1';
    
    var tableBody = document.createElement('TBODY');
    table.appendChild(tableBody);
      
    for (var i=0; i<3; i++){
       var tr = document.createElement('TR');
       tableBody.appendChild(tr);
       
       for (var j=0; j<4; j++){
           var td = document.createElement('TD');
           td.width='75';
           td.appendChild(document.createTextNode("Cell " + i + "," + j));
           tr.appendChild(td);
       }
    }
    myTableDiv.appendChild(table);
    
}
 
function load() {
    console.log("Page load finished");
}
