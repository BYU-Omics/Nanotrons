
var socket = io.connect('http://127.0.0.1:5000');

var current_settings;

// This section applies properties needed for the collapsible tabs to work
var coll = document.getElementsByClassName("collapsible");
var i;
for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
            content.style.maxHeight = null;
        } 
        else {
            content.style.maxHeight = content.scrollHeight + "px";
        } 
    });
}

function openControlInput(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent1");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks1");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

function open3DSetting(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent2");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks2");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

function activateDefaultTab(collapsible) {
    if (collapsible == 'xbox_collapsible') {
        document.getElementById("defaultOpen1").click();
    }
    else {
        document.getElementById("defaultOpen2").click();
    }
}

// This method sends an updated version of the settings dictionary to the server
function send_updated_setting(setting_name, new_value) {
    socket.emit("updated_setting", [setting_name, new_value]);
}

function toggle_visibility(id1, id2, id3) {
    comp1 = document.getElementById(id1);
    comp2 = document.getElementById(id2);
    comp3 = document.getElementById(id3);

    comp1.hidden = !comp1.hidden;
    comp2.hidden = !comp2.hidden;
    comp3.hidden = !comp3.hidden;
}

function adjust_btn_pressed(current_value_id, options_id, save_btn_id) {
    toggle_visibility(current_value_id, options_id, save_btn_id);
}

function save_btn_pressed(setting_name, current_value_id, options_id, save_button_id, unit) {
    var current_value_comp = document.getElementById(current_value_id);
    var options_comp = document.getElementById(options_id);

    var option_selected = options_comp.options[options_comp.selectedIndex].text;
    current_settings[setting_name] = option_selected;
    current_value_comp.innerHTML = option_selected + " " + unit;
    send_updated_setting(setting_name, option_selected);
    toggle_visibility(current_value_id, options_id, save_button_id);
}

socket.emit("get_current_settings"); // Get the dictionary with all the current settings of the system (asks for a dictionary)

socket.emit("get_dynamic_selects_options"); // Get the list of models of syringes that will be displayed in the dropdown list of syringe model selection

var static_selects = {
    refresh_rate: {
        id: "coordinate_refresh_rate",
        button_label: "Coordinate Refresh Rate",
        unit: "[sec]"
    },
    syringe_default_speed: {
        id: "syringe_default_speed",
        button_label: "Syringe Default Speed",
        unit: "[mm/s]"
    },
    x_axis_step_size: {
        id: "x_axis_step_size",
        button_label: "Step Size",
        unit: "[mm]"
    },
    x_axis_step_speed: {
        id: "x_axis_step_speed",
        button_label: "Step Speed",
        unit: "[mm/s]"
    },
    x_axis_gearbox: {
        id: "x_axis_gearbox",
        button_label: "Gearbox",
        unit: ""
    },
    x_axis_orientation: {
        id: "x_axis_orientation",
        button_label: "Axis Orientation",
        unit: ""
    },
    y_axis_step_size: {
        id: "y_axis_step_size",
        button_label: "Step Size",
        unit: "[mm]"
    },
    y_axis_step_speed: {
        id: "y_axis_step_speed",
        button_label: "Step Speed",
        unit: "[mm/s]"
    },
    y_axis_gearbox: {
        id: "y_axis_gearbox",
        button_label: "Gearbox",
        unit: ""
    },
    y_axis_orientation: {
        id: "y_axis_orientation",
        button_label: "Axis Orientation",
        unit: ""
    },
    z_axis_step_size: {
        id: "z_axis_step_size",
        button_label: "Step Size",
        unit: "[mm]"
    },
    z_axis_step_speed: {
        id: "z_axis_step_speed",
        button_label: "Step Speed",
        unit: "[mm/s]"
    },
    z_axis_gearbox: {
        id: "z_axis_gearbox",
        button_label: "Gearbox",
        unit: ""
    },
    z_axis_orientation: {
        id: "z_axis_orientation",
        button_label: "Axis Orientation",
        unit: ""
    }
};

var dynamic_selects = {
    syringe_model: {
        id: "syringe_model",
        button_label: "Syringe Model",
        unit: ""
    }
}

var static_select_options = {
    refresh_rate: [0.05, 0.1, 0.5],
    syringe_default_speed: [1, 0.5, 0.1],
    x_axis_step_size: [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.5],
    x_axis_step_speed: [1, 0.5, 0.1, 2],
    x_axis_gearbox: [[0.2,1,4], [0.05, 0.5, 4], [0.05, 2, 4]],
    x_axis_orientation: [1, -1],
    y_axis_step_size: [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.5],
    y_axis_step_speed: [1, 0.5, 0.1, 2],
    y_axis_gearbox: [[0.2,1,4], [0.05, 0.5, 4], [0.05, 2, 4]],
    y_axis_orientation: [1, -1],
    z_axis_step_size: [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.5],
    z_axis_step_speed: [1, 0.5, 0.1, 2],
    z_axis_gearbox: [[0.2,1,4], [0.05, 0.5, 4], [0.05, 2, 4]],
    z_axis_orientation: [1, -1]
}

// This method adds the current values to all the settings of the webpage
function receive_current_settings(received_settings) {
    current_settings = received_settings;
}

function fill_selects_options(dynamic_selects_options) {

    var static_select_options_length = Object.keys(static_selects).length;
    var dynamic_select_options_length = Object.keys(dynamic_selects).length;

    // Create the static select components and attach their corresponding options
    for (var i=0; i < static_select_options_length; i++) {
        var key = Object.keys(static_selects)[i];
        addSelect(static_selects[key], static_select_options[key], current_settings[static_selects[key].id])
    }

    // Create the synamic select components and attach their corresponding options
    for (var i=0; i < dynamic_select_options_length; i++) {
        var key = Object.keys(dynamic_selects)[i];
        addSelect(dynamic_selects[key], dynamic_selects_options[key], current_settings[dynamic_selects[key].id])
    }
}

function addSelect(select_object, options_list, current_value) {
    var id = select_object.id;
    var label = select_object.button_label;
    var unit = select_object.unit;
    var optionsHTML = "";
    for (let option of options_list) {
        optionsHTML += `<option>${option}</option>`;
    }
    var div = document.getElementById(id);
    var div_text= `
    <button type="button" id="${id}_btn" onclick="adjust_btn_pressed('current_${id}', 'select_${id}', 'save_${id}')">${label}</button>
    <label id="current_${id}">${current_value} ${unit}</label>
    <select id="select_${id}" hidden="true">
        <option value="default" selected>- Select Option -</option>
        ${optionsHTML}
    </select>
    <button id="save_${id}" hidden="true" onclick="save_btn_pressed('${id}', 'current_${id}', 'select_${id}', 'save_${id}', '${unit}')">SAVE</button><br>
    `;
    div.insertAdjacentHTML("afterbegin", div_text);
}

socket.on('current_settings', receive_current_settings);

socket.on('dynamic_selects_options', fill_selects_options);
