var socket = io.connect('http://127.0.0.1:5000');

socket.emit("reconnect_coordinator")