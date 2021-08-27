var socket = io.connect('http://127.0.0.1:5000');
var home_button = document.getElementById("back_home");

socket.emit("start_manual_control_window");
socket.emit("give_me_coordinates");

home_button.addEventListener("click", function() {
    socket.emit("stop_manual_control_window");
});

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
    socket.emit("take_picture", "Manual Control Pictures")
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
