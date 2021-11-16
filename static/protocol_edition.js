var socket = io.connect('http://127.0.0.1:5000/');
var save_button = document.getElementById("comp-kv5z3mgq");

//PROCOL INFORMATION VARIABLES
// Get select components by id
var protocol_name = document.getElementById("protocol_name");
var protocol_author = document.getElementById("protocol_author");

function send_protocol_info() {
    console.log(protocol_name)
    console.log(protocol_author)
    socket.emit("send_protocol_info", [protocol_name, protocol_author])
}
