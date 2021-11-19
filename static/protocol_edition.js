var socket = io.connect('http://127.0.0.1:5000/');
var save_button = document.getElementById("comp-kv5z3mgq");
var add_command_button = document.getElementById("compile_commmand");


//PROCOL INFORMATION VARIABLES
// Get select components by id
var labware_name = document.getElementById("files_stored");
var filename = document.getElementById("filename");
var voided_plates = document.getElementById("comp-kv1w6jwo");
var list_of_commands = document.getElementById("list_of_commands");
var command = document.getElementById("commands");
var author = document.getElementById("author");
var description = document.getElementById("description");
var waste_water_well = document.getElementById("waste_water_well");
var wash_water_well = document.getElementById("wash_water_well");
var clean_water_well = document.getElementById("clean_water_well");

function send_protocol_info() {
    console.log(protocol_name.innerHTML)
    console.log(protocol_author.innerHTML)
    socket.emit("send_protocol_info", [protocol_name, protocol_author])
}

function input_check(input_text) {

    // Check if the .json extension was provided
    if (input_text.includes(" ")) {
        return [false, "The \"name\" should not include spaces"];
    }

    // Check for invalid characters
    var invalid_characters = ["\\", "/", ".", "#", ":", ";", "\"", "\'", "*", "?", "<", ">"]; // --->    \ / . # : ; " ' * ? < >
    for (var i=0; i < invalid_characters.length; i++){
        if (input_text.includes(invalid_characters[i])) {
            return [false, "Invalid character entered: " + invalid_characters[i]];
        }
    }

    // // Check for file name duplicity
    // if (stored_files_list.includes(input_text+".json")){ // This check is included at the end so that we can manually add the ".json" without running the risk of the extension being included twice (it was already checked its absence above)
    //     return [false, "Name already associated with another labware file"];
    // }

    return [true, "All tests passed"]; // If the function gets this far means that all the previous tests failed (they weren't succesful at proving bad input)
}

function command_selected() {
    console.log(command.value)
}

add_command_button.addEventListener("click", function(){
    command_selected(command.value)
});

save_button.addEventListener("click", function(){
    console.log("Labware name: " + labware_name.value)
    console.log("File name: "+filename.value)
    console.log("author: "+author.value)
    socket.emit("send_protocol_info", [labware_name.value, 
                                       filename.value, 
                                       voided_plates.value, 
                                       list_of_commands.value, 
                                       author.value,
                                       description.value,
                                       waste_water_well.value,
                                       wash_water_well.value,
                                       clean_water_well.value])
    // var good_input = input_check(filename_value.value); // [boolean, description]
    // var feedback = document.getElementById("feedback");
    // if (good_input[0]) {
        
    //     feedback.innerText = "  Labware correctly saved to file " + filename_value + "";
    // }
    // else {
    //     feedback.innerText = "  INPUT ERROR. "+ good_input[1];
    // }

});