var form = document.querySelector("form");

var socket = io.connect('http://127.0.0.1:5000');

var calibrated_chips = document.getElementById("calibrated_chips");
var calibrated_plates = document.getElementById("calibrated_plates");
var delete_button = document.getElementById("delete_labware");
var delete_form = document.getElementById("delete_form");

socket.emit("give_me_current_labware");

socket.on("here_current_labware", function(labware_dict) {
    console.log(labware_dict);

    // Update the list of chips
    for (var key in labware_dict['chips']){
        var node = document.createElement('li'); // Create a list element
        node.appendChild(document.createTextNode(key)); // Append a text node to the list element node
        calibrated_chips.appendChild(node); // Add the node to the labware list
    }
    
    // Update the list of plates
    for (var key in labware_dict['plates']){
        var node = document.createElement('li'); // Create a list element
        node.appendChild(document.createTextNode(key)); // Append a text node to the list element node
        calibrated_plates.appendChild(node); // Add the node to the labware list
    }
});

delete_button.addEventListener("click", function() {
    // Toggle hidden feature of the text input 
    delete_form.hidden = !delete_form.hidden;
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