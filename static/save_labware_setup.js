
var form = document.querySelector("form");

var socket = io.connect('http://127.0.0.1:5000');

var stored_files_component = document.getElementById("current_files");
var save_button = document.getElementById("save_to_file_btn");
var file_name_input = document.getElementById("file_name");

var stored_files_list = ["holiwi.json"];

socket.emit("available_saved_labware_files");
console.log("Loading page")

socket.on("saved_labware_files", function(files_list) {
    stored_files_list = files_list;
    console.log(stored_files_list);
    for (var i = 0; i < files_list.length / 2 ; i++){
        var node = document.createElement('li'); // Create a list element
        node.appendChild(document.createTextNode(files_list[i])); // Append a text node to the list element node
        stored_files_component.appendChild(node); // Add the node to the labware list
    }   
});

function input_check(input_text) {

    // Check if the .json extension was provided
    if (input_text.includes(".json")) {
        return [false, "The \".json\" extension should not be included"];
    }

    // Check for invalid characters
    var invalid_characters = ["\\", "/", ".", "#", ":", ";", "\"", "\'", "*", "?", "<", ">"]; // --->    \ / . # : ; " ' * ? < >
    for (var i=0; i < invalid_characters.length; i++){
        if (input_text.includes(invalid_characters[i])) {
            return [false, "Invalid character entered: " + invalid_characters[i]];
        }
    }

    // Check for file name duplicity
    if (stored_files_list.includes(input_text+".json")){ // This check is included at the end so that we can manually add the ".json" without running the risk of the extension being included twice (it was already checked its absence above)
        return [false, "Name already associated with another labware file"];
    }

    return [true, "All tests passed"]; // If the function gets this far means that all the previous tests failed (they weren't succesful at proving bad input)
}


save_button.addEventListener("click", function(){
    var file_name = file_name_input.value;
    var good_input = input_check(file_name); // [boolean, description]
    var feedback = document.getElementById("feedback");
    if (good_input[0]) {
        socket.emit("save_labware_setup", file_name);
        feedback.innerText = "  Labware correctly saved to file " + "\"" + file_name + ".json\"";
    }
    else {
        feedback.innerText = "  INPUT ERROR. "+ good_input[1];
    }

});

