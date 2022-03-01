var socket = io.connect('http://127.0.0.1:5000');

var run_protocol_button = document.getElementById("run_protocol");
var protocolOptions = document.getElementById("protocols"); // Dropdown list that shows the available models
var display_protocol_button = document.getElementById("comp-kyvxez3y");
var show_calibration_button = document.getElementById("comp-kyvxfeoy");
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

var calibrated_chips = document.getElementById("calibrated_chips");
var calibrated_plates = document.getElementById("calibrated_plates");

var contents = ""
var protocols = {}
var script_to_display = "error" // save as error until over written
var protocol_to_display = "error"
var calibration_to_display = "error"
var syringe_to_display = "error"

var json_data = "" // will hold the json data from the script
var python_data = ""

var list_of_plates_in_html = []
// asks python to send the list of scripts

socket.emit("get_available_protocols")
console.log("emited: get_available_protocols")
// socket.emit("give_me_protocol_python")

// listens for the list of available scripts
socket.on('protocols_available', function(received_protocols) {
    protocols = received_protocols; // save list in scripts variable
    console.log("protocol received")
    fill_protocol_drop_down() // add the options to the list
}); 

socket.on('display_contents', function(file_contents) {
    python_file_contents = file_contents
    display_protocol_button.disabled = true;
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


// this runs each time you select an option from the script list
function option_select_protocol(){
    // This either blocks or unblocks the submit button
    var selected_protocol = protocolOptions.options[ protocolOptions.selectedIndex ].value;
    protocol_to_display = selected_protocol; // set variable to the selected value
    console.log(selected_protocol)
    socket.emit("set_protocol_filename", protocol_to_display)
    if ( selected_protocol != "- Select a Protocol -" ) { // if you select something from the list
        display_protocol_button.disabled = false; // enable the button
        show_calibration_button.disabled = false;
    }
    else { // if you select the instructions from the list
        display_protocol_button.disabled = true; // disable button
        show_calibration_button.disabled = true;
    }
}

// this runs when you click the display script button
display_protocol_button.addEventListener("click", function() {
    // clear_protocol_Table() // clear out the old table data
    console.log("clearing table")
});

socket.on('protocol_python_labware', function(file_name){
    console.log("Labware for protocol: ", file_name)
    var labware_name_file = document.getElementById("calibration_file")
    labware_name_file.innerHTML = file_name
    // socket.emit("delete_current_labware")
});

socket.on('protocol_python_author', function(author) {
    console.log("Author for protocol: ", author)
    var author_name = document.getElementById("author")
    author_name.innerHTML = author
});  

socket.on('protocol_python_description', function(description) {
    console.log("Description of protocol: ", description)
    var description_text = document.getElementById("description")
    description_text.innerHTML = description
});  


socket.on('protocol_python_chips', function(chips) {
    console.log("Description of protocol: ", chips)
    var chips_text = document.getElementById("chips")
    chips_text.innerHTML = chips
});  


socket.on('protocol_python_plates', function(plates) {
    console.log("Description of protocol: ", plates[0])
    var plates_text = document.getElementById("plates")
    plates_text.innerHTML = plates
});  


socket.on('protocol_python_locations', function(locations) {
    console.log("Description of protocol: ", locations[1])
    var locations_text = document.getElementById("locations")
    locations_text.innerHTML = locations
});  


// listens for the json data
socket.on('protocol_python_data', function(python_lines_list) {
    console.log("protocols received")
    python_data = python_lines_list; // save list in scripts variable
    var content = document.getElementById("file_contents")
    
    text_area_left = '<textarea id="w3review" name="w3review" rows="4" cols="50">'
    text_area_right = '</textarea>'
    text = "<br>" + text_area_left
    for (let i = 0; i < python_data.length; i++) {
        if (python_data[i][0] == '#') {
            text +=  python_data[i] ;
        } else {
            
            text += python_data[i] ;
        }
    }
    content.innerHTML = text + text_area_right + "<br>"    
});  

function display_contents() {
    socket.emit("display_contents")
}

function display_labware() {
    socket.emit("give_me_current_labware")
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
    console.log("Run protocol button pressed")
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
      
    var table = document.createElement('TABLE');
    table.border='1';
    
    var tableBody = document.createElement('TBODY');
    table.appendChild(tableBody);
      
    for (var i = 0; i < 3; i++){
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

socket.on("labware_locations_dict", function(labware_slot) {
    console.log(labware_slot);
    console.log(calibrated_plates);
    console.log(calibrated_chips);
    // socket.emit("delete_current_labware")
    if (calibrated_plates || calibrated_chips) {
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
        show_calibration_button.disabled = true;
    } else {
        console.log("Calibration already populated.")
    } 
});
