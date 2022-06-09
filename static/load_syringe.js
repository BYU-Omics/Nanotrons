var socket = io.connect('http://127.0.0.1:5000');

var files_list = ["mock_file1.json", "mock_file2.json", "mock_file3.json", "mock_file4.json"];

socket.emit("available_saved_syringe_files");

// Get select components by id
var syringe_select = document.getElementById('syringe_type')
var load_syringe = document.getElementById("load_syringe");
var previous_labware_selected = "";
populate_file_options(); // This is only needed for testing, when the system is connected to the server this is redundant since it's already done when the socket receives the labware_summary

//The socket.on event is placed after the testing call for populate_file_options() to make sure the testing happens before actual data is received and processed (otherwise test data would overwrite actual data)
socket.on("saved_syringe_files", function(received_files_list) {
    files_list = received_files_list;
    // Empty test options added
    reset_files_options();
    // Populate options for the files dropdown list here
    populate_file_options();
});

function reset_files_options() {
    // Erase all the options inside the dropdown list (select object)
    var length = syringe_select.options.length;

    // The following for loop itertes from largest index to smalles since as items are removed, the length of the array decreases
    for (var i = length - 1; i >= 0; i--) {
        syringe_select.remove(i);
    };

    // Add instruction option ()
    var option = document.createElement("option"); 
    option.text = "- Select a Syringe Model -";
    option.value = "default";
    syringe_select.add(option);
}

function populate_file_options() {
    for (var i = 0; i < files_list.length; i++){
        var new_option = document.createElement("option"); // Create an option element
        new_option.text = files_list[i]; // Add text to the option
        syringe_select.add(new_option); // Attach the option element to the syringe_select component
    }
}

function syringe_model_onclick() {
    console.log("syringe_stored_onclick called!");
    var option_selected = syringe_select.options[ syringe_select.selectedIndex ].value;
    console.log(option_selected);

    if (option_selected != "default") {
        // Toggle on LOAD button visibility if there is an option selected other than the default
        load_syringe.disabled = false;
    }

    else {
        // Toggle off LOAD button visibility if the selected option is the default
        load_syringe.disabled = true;
    }

}

function load_syringe_listener() {
    var file_name = syringe_select.options[ syringe_select.selectedIndex ].value;
    console.log("LOAD Syringe button pressed :D");
    console.log(file_name);
    socket.emit("load_syringe_setup", file_name); // Send the command! :D
    var feedback = document.getElementById("user_feedback");
    feedback.innerHTML = `${file_name} has been loaded to the system`;
}
