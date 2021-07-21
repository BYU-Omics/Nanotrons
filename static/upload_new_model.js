$(document).ready( function(){

    var radio1 = document.getElementById("Container1");
    var radio2 = document.getElementById("Container2");
    var file_upload = document.getElementById("file_upload");
    var submit_button = document.getElementById("submit_btn");

    radio1.onclick = function() {
        file_upload.disabled = false;
        submit_button.disabled = false;
    };

    radio2.onclick = function() {
        file_upload.disabled = false;
        submit_button.disabled = false;
    };

  })