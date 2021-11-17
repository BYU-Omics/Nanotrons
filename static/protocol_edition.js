var socket = io.connect('http://127.0.0.1:5000/');
var save_button = document.getElementById("comp-kv5z3mgq");

//PROCOL INFORMATION VARIABLES
// Get select components by id
var protocol_name = document.getElementById("protocol_name");
var protocol_author = document.getElementById("protocol_author");

function send_protocol_info() {
    console.log(protocol_name.value)
    console.log(protocol_author.value)
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

save_button.addEventListener("click", function(){
    var protocol_name = protocol_name.value;
    var protocol_author = protocol_author.value;
    var good_input = input_check(file_name); // [boolean, description]
    var feedback = document.getElementById("feedback");
    if (good_input[0]) {
        socket.emit("send_protocol_info", [protocol_name, protocol_author])
        feedback.innerText = "  Labware correctly saved to file " + "\"" + file_name + ".json\"";
    }
    else {
        feedback.innerText = "  INPUT ERROR. "+ good_input[1];
    }

});