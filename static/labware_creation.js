var socket = io.connect('http://127.0.0.1:5000');

var labware_models = {
    "chips": ["mock_chip_model_1", "mock_chip_model_2", "mock_chip_model_3", "mock_chip_model_4"],
    "plates":["mock_plate_model_1", "mock_plate_model_2"],
    "syringes":["mock_syringe_model_1", "mock_syringe_model_2", "mock_syringe_model_3"]
}; // Initial values are a default for testing without connecting to the equipment

// Main body divs
var models_table_div = document.getElementById("models_table_div");
var user_inputs_div = document.getElementById("user_input_div");
var user_summary_div = document.getElementById("user_summary_div");
var confirmation_feedback_div = document.getElementById("confirmation_feedback");

// Radio Input Elements
var chip_radio_input = document.getElementById("chip");
var plate_radio_input = document.getElementById("plate");
var syringe_radio_input = document.getElementById("syringe");

// Divs that pop up depending on the radio input selected
var chip_properties_div = document.getElementById("chip_properties");
var plate_properties_div = document.getElementById("plate_properties");
var syringe_properties_div = document.getElementById("syringe_properties");

//Input fields for a Chip element
var chip_new_model_name = document.getElementById("chip_new_model_name");
var chip_grid_rows = document.getElementById("chip_grid_rows");
var chip_grid_columns = document.getElementById("chip_grid_columns");
var chip_point_distance = document.getElementById("chip_point_distance");
var chip_well_distance = document.getElementById("chip_well_distance");

//Input fields for a Plate element
var plate_new_model_name = document.getElementById("plate_new_model_name");
var plate_grid_rows = document.getElementById("plate_grid_rows");
var plate_grid_columns = document.getElementById("plate_grid_columns");
var plate_pot_distance_r = document.getElementById("plate_pot_distance_r");
var plate_pot_distance_c = document.getElementById("plate_pot_distance_c");
var plate_pot_depth = document.getElementById("plate_pot_depth");

//Input fields for a Syringe element
var syringe_new_model_name = document.getElementById("syringe_new_model_name");
var syringe_volume = document.getElementById("syringe_volume");
var syringe_inner_diameter = document.getElementById("syringe_inner_diameter");

// Submission buttons
var back_to_edit_mode_btn = document.getElementById("back_to_edit");
var confirm_parameters_btn = document.getElementById("confirm_parameters");
var create_model_btn = document.getElementById("create_model");

// Global variable for the properties to be sent through the socket
var final_new_model_properties;

populate_registered_models(); // Calling function for testing purposes before actual data arrives

socket.emit("get_labware_models");

socket.on('models_available', function(received_models) {
    labware_models = received_models;

    // Reset all the lists
    reset_model_lists();
    // Populate chip, plate, and syringe lists
    populate_registered_models();

});

// ----------------------- CAPTURE INPUT METHODS

function extract_all_inputs() {
    // console.log("extract_all_inputs()");
    // Either return the data or return false if not all the required fields are filled out

    if (chip_radio_input.checked) {
        var properties = extract_chip_fields();
        // console.log("final chip properties", properties);
        return properties;
    }

    if (plate_radio_input.checked) {
        var properties = extract_plate_fields();
        // console.log("final plate properties", properties);
        return properties;
    }

    if (syringe_radio_input.checked) {
        var properties = extract_syringe_fields();
        // console.log("final syringe properties", properties);
        return properties;
    }
    // It only gets here if nothing was returned (meaning no radio buttons were pressed when this function was called)
    console.log("NO COMPONENT TYPE SELECTED (radio buttons)");
}

function extract_chip_fields() {
    var chip_elements_ids = ["chip_new_model_name", "chip_grid_rows", "chip_grid_columns", "chip_point_distance", "chip_well_distance"];
    var chip_properties = {};
    chip_properties.component_type = "Chip";
    // Get the info from the static fields

    for (var index=0; index < chip_elements_ids.length; index++) {
        var value_provided = check_if_empty(chip_elements_ids[index]);
        // console.log(`value_provided: ${chip_elements_ids[index]}`, value_provided);
        if (value_provided == null) {
            return false;
        }
        else {
            chip_properties[chip_elements_ids[index]] = value_provided;
        }
    }
    // console.log("Static properties of object", chip_properties);

    // Get the info from the dynamic fields

    var rows = parseInt(chip_grid_rows.value)
    var columns = parseInt(chip_grid_columns.value);

    // Get info from the row types dropdown lists
    var row_types = [];
    for (var i=0; i<rows; i++) {
        var select_component = document.getElementById(`row_type_${i}`);
        var row_type_selected = select_component.value;
        if (row_type_selected == "default") {
            console.log("CHIP ROW TYPE ERROR, DEFAULT SELECTED");
            return false;
        }
        else {
            row_types.push(row_type_selected);
        }
    }
    // console.log("row_types", row_types);
    chip_properties.row_types = row_types;

    // Get info from the nicknames table
    var provided_nicknames = [];
    var nicknames_amount = 0;
    if ( (rows != NaN) && (columns != NaN) ) {
        nicknames_amount = rows * columns;
    }

    else {
        console.log("CHIP ROWS OR COLUMNS INPUT ERROR");
    }

    var well_number = 0;
    for (var row = 0; row<rows; row++) {
        var row_nicknames = [];
        for (var col=0; col<columns; col++) {
            var input_component = document.getElementById(`well_${well_number}`);
            if (input_component.value == "") {
                console.log(`Well #${well_number} has no input value`);
                return false;
            }
            else {
                row_nicknames.push(input_component.value);
            }
            well_number++;
        }
        provided_nicknames.push(row_nicknames)
    }
    // console.log("provided_nicknames", provided_nicknames);

    chip_properties.nicknames = provided_nicknames;

    // return the object (if it gets to this point, nothing was returned before which means there were no null input fields)
    return chip_properties;

}

function extract_plate_fields() {
    var plate_elements_ids = ["plate_new_model_name", "plate_grid_rows", "plate_grid_columns", "plate_pot_distance_r", "plate_pot_distance_c",  "plate_pot_depth"];
    var plate_properties = {};
    plate_properties.component_type = "Plate";
    // Get the info from the static fields

    for (var index=0; index < plate_elements_ids.length; index++) {
        var value_provided = check_if_empty(plate_elements_ids[index]);
        // console.log(`value_provided: ${plate_elements_ids[index]}`, value_provided);
        if (value_provided == null) {
            return false;
        }
        else {
            plate_properties[plate_elements_ids[index]] = value_provided;
        }
    }
    // console.log("Static properties of object", plate_properties);
    
    // Get the info from the dynamic fields

    var rows = parseInt(plate_grid_rows.value)
    var columns = parseInt(plate_grid_columns.value);

    // Get info from the nicknames table
    var provided_nicknames = [];
    var nicknames_amount = 0;
    if ( (rows != NaN) && (columns != NaN) ) {
        nicknames_amount = rows * columns;
    }

    else {
        console.log("PLATE ROWS OR COLUMNS INPUT ERROR");
    }
    
    var pot_number = 0;
    for (var row = 0; row<rows; row++) {
        var row_nicknames = [];
        for (var col=0; col<columns; col++) {
            var input_component = document.getElementById(`pot_${pot_number}`);
            if (input_component.value == "") {
                console.log(`Pot #${pot_number} has no input value`);
                return false;
            }
            else {
                row_nicknames.push(input_component.value);
            }
            pot_number++;
        }
        provided_nicknames.push(row_nicknames)
    }
    // console.log("provided_nicknames", provided_nicknames);

    plate_properties.nicknames = provided_nicknames;

    // return the object (if it gets to this point, nothing was returned before which means there were no null input fields)
    return plate_properties;

}

function extract_syringe_fields() {
    var syringe_elements_ids = ["syringe_new_model_name", "syringe_volume", "syringe_inner_diameter"];
    var syringe_properties = {};
    syringe_properties.component_type = "Syringe";
    // Get the info from the static fields

    for (var index=0; index < syringe_elements_ids.length; index++) {
        var value_provided = check_if_empty(syringe_elements_ids[index]);
        // console.log(`value_provided: ${syringe_elements_ids[index]}`, value_provided);
        if (value_provided == null) {
            return false;
        }
        else {
            syringe_properties[syringe_elements_ids[index]] = value_provided;
        }
    }
    // console.log("Static properties of object", syringe_properties);

    // return the object (if it gets to this point, nothing was returned before which means there were no null input fields)
    return syringe_properties;
}

function write_user_summary(model_properties) {
    var component_type = model_properties.component_type;
    var additional_div_text = `
    <h3>New ${component_type} Model Summary</h3><br>
    `;

    if (component_type == "Chip") {
        var well_nicknames = model_properties.nicknames;
        var rows = model_properties.chip_grid_rows;
        var columns = model_properties.chip_grid_columns;
        additional_div_text += `
        <label class="field_label"><u><b>Model: </b></u></label> <label>${model_properties.chip_new_model_name}</label><br>
        <label class="field_label"><u><b>Grid: </b></u></label> <label>${rows} x ${columns}</label><br>
        <label class="field_label"><u><b>Point Distance: </b></u></label> <label>${model_properties.chip_point_distance}</label><br>
        <label class="field_label"><u><b>Well Distance: </b></u></label> <label>${model_properties.chip_well_distance}</label><br>
        <label class="field_label"><u><b>Row Types: </b></u></label> <label>${model_properties.row_types}</label><br>
        <label class="field_label"><u><b>Well Names: </b></u></label><br>
        `
        additional_div_text += `<table>`; // Open the table
        for (var row=0; row < rows; row++) {
            // Open row
            additional_div_text += `<tr>`;
            for (var col=0; col < columns; col++) {
                if (col == 0) {
                    additional_div_text += `<th>Row #${row+1}</th>`
                }
                // Add column data
                additional_div_text += `<td>${well_nicknames[row][col]}</td>`;
            }
            // Close row
            additional_div_text += `</tr>`;
        }
        additional_div_text += `</table>`; // Close the table
    }

    if (component_type == "Plate") {
        var pot_nicknames = model_properties.nicknames;
        var rows = model_properties.plate_grid_rows;
        var columns = model_properties.plate_grid_columns;
        additional_div_text += `
        <label class="field_label"><u><b>Model: </b></u></label> <label>${model_properties.plate_new_model_name}</label><br>
        <label class="field_label"><u><b>Grid: </b></u></label> <label>${rows} x ${columns}</label><br>
        <label class="field_label"><u><b>Pot Distance: </b></u></label> <label>${model_properties.plate_pot_distance_r}</label><br>
        <label class="field_label"><u><b>Pot Distance: </b></u></label> <label>${model_properties.plate_pot_distance_c}</label><br>
        <label class="field_label"><u><b>Pot Depth: </b></u></label> <label>${model_properties.plate_pot_depth}</label><br>
        <label class="field_label"><u><b>Pot Names: </b></u></label><br>
        `
        additional_div_text += `<table>`; // Open the table
        for (var row=0; row < rows; row++) {
            // Open row
            additional_div_text += `<tr>`;
            for (var col=0; col < columns; col++) {
                if (col == 0) {
                    additional_div_text += `<th>Row #${row+1}</th>`
                }
                // Add column data
                additional_div_text += `<td>${pot_nicknames[row][col]}</td>`;
            }
            // Close row
            additional_div_text += `</tr>`;
        }
        additional_div_text += `</table>`; // Close the table
    }

    if (component_type == "Syringe") {
        additional_div_text += `
        <label class="field_label"><u><b>Model: </b></u></label> <label>${model_properties.syringe_new_model_name}</label><br>
        <label class="field_label"><u><b>Volume: </b></u></label> <label>${model_properties.syringe_volume} cc</label><br>
        <label class="field_label"><u><b>Inner Diameter: </b></u></label> <label>${model_properties.syringe_inner_diameter} mm</label><br>
        `
    }

    user_summary_div.insertAdjacentHTML("afterbegin", additional_div_text);
}

// This method receives an id and checks if the html component associated to that id has content. It either returns null or the value contained in that html element
function check_if_empty(id) {
    var html_element = document.getElementById(id);
    if (html_element.value == "") {
        return null
    }
    else {
        return html_element.value
    }
}

// ----------------------- DYNAMIC INPUT FIELDS METHODS - CHIPS

function check_chip_grid_inputs() {
    var row_input = chip_grid_rows.value;
    var col_input = chip_grid_columns.value;
    var row_input_number = parseInt(row_input); // The only way this will not be an integer is if the field was left blank or the user entered something other than a number
    var col_input_number = parseInt(col_input);
    var chip_grid_feedback = document.getElementById("chip_grid_feedback");
    chip_grid_feedback.innerHTML = "";

    if ( (!isNaN(row_input_number)) && (!isNaN(col_input_number)) ){
        // This means both row and col inputs are numbers
        // Call method that creates the dynamic html code
        create_chip_fields(row_input_number, col_input_number);
    }

    else {
        // Inputs were wrong (they're either empty or user entered something other than a number in at least one of the fields)
        if ((row_input != "") && (col_input != "")) {
            // Both inputs have content, but at least one of them is in the wrong format, so write a feedback line
            chip_grid_feedback.innerHTML = " ERROR! Only numbers (integers) allowed for grid size"
        }
    }
}

function create_chip_fields(rows, columns) {
    // Create the options for the row types (all big, all small, intercalated)
    create_row_type_options(rows);

    // Create table for the user to provide the nickname of each well
    create_chip_nicknames_table(rows, columns);
}

function create_chip_nicknames_table(rows, columns) {
    var nicknames_div = document.getElementById("chip_nicknames_div");
    nicknames_div.innerHTML = ``; // Empty the content with every call so that the previous table (in case the user specifies it many times) is deleted
    var nicknames_table = `<table>`; // Open the table
    var well_number = -1;

    for (var row=0; row < rows; row++) {
        // Open row
        nicknames_table += `<tr>`;
        for (var col=0; col < columns; col++) {
            if (col == 0) {
                nicknames_table += `<th>Row #${row+1}</th>`
            }
            well_number += 1;
            // console.log("well_number", well_number);
            // Add column data
            nicknames_table += `<td><input size="2" id="well_${well_number}"></td>`;
        }
        // Close row
        nicknames_table += `</tr>`;
    }
    nicknames_table += `</table>`; // Close the table
    nicknames_div.insertAdjacentHTML("afterbegin", nicknames_table);
}

function create_row_type_options(rows) {
    var row_types_div = document.getElementById("chip_row_types_div");
    row_types_div.innerHTML = ``;
    var row_types_text = ``;

    for (var row=0; row < rows; row++) {
        row_types_text+= `
            &emsp;<label>- Row #${row+1}: </label>
            <select id="row_type_${row}">
                <option value="default"> - Select a type for row #${row+1} - </option>
                <option value="B">B (all wells are big)</option>
                <option value="S">S (all wells are small)</option>
                <option value="BS">BS (intercalated well size)</option>
            </select><br>
        `
    }
    row_types_text+= `<br>`;
    row_types_div.insertAdjacentHTML("afterbegin", row_types_text);
}

// ----------------------- DYNAMIC INPUT FIELDS METHODS - PLATES

function check_plate_grid_inputs() {
    var row_input = plate_grid_rows.value;
    var col_input = plate_grid_columns.value;
    var row_input_number = parseInt(row_input); // The only way this will not be an integer is if the field was left blank or the user entered something other than a number
    var col_input_number = parseInt(col_input);
    var plate_grid_feedback = document.getElementById("plate_grid_feedback");
    plate_grid_feedback.innerHTML = "";

    if ( (!isNaN(row_input_number)) && (!isNaN(col_input_number)) ){
        // This means both row and col inputs are numbers
        // Call method that creates the dynamic html code
        create_plate_nicknames_table(row_input_number, col_input_number);
    }

    else {
        // Inputs were wrong (they're either empty or user entered something other than a number in at least one of the fields)
        if ((row_input != "") && (col_input != "")) {
            // Both inputs have content, but at least one of them is in the wrong format, so write a feedback line
            plate_grid_feedback.innerHTML = " ERROR! Only numbers (integers) allowed for grid size"
        }
    }
}

function create_plate_nicknames_table(rows, columns) {
    var nicknames_div = document.getElementById("plate_nicknames_div");
    nicknames_div.innerHTML = ``; // Empty the content with every call so that the previous table (in case the user specifies it many times) is deleted
    var nicknames_table = `<table>`; // Open the table
    var pot_number = -1;

    for (var row=0; row < rows; row++) {
        // Open row
        nicknames_table += `<tr>`;
        for (var col=0; col < columns; col++) {
            if (col == 0) {
                nicknames_table += `<th>Row #${row+1}</th>`
            }
            pot_number += 1;
            // console.log("well_number", well_number);
            // Add column data
            nicknames_table += `<td><input size="2" id="pot_${pot_number}"></td>`;
        }
        // Close row
        nicknames_table += `</tr>`;
    }
    nicknames_table += `</table>`; // Close the table
    nicknames_div.insertAdjacentHTML("afterbegin", nicknames_table);
}

// ----------------------- EXISTING FILES DISPLAY METHODS

function populate_registered_models() {

    var chips_list = labware_models["chips"];
    var plates_list = labware_models["plates"];
    var syringes_list = labware_models["syringes"];
    var chips_amount = chips_list.length;
    var plates_amount = plates_list.length;
    var syringes_amount = syringes_list.length;

    var table_rows = Math.max(chips_amount, plates_amount, syringes_amount);

    // Empty previous content
    models_table_div.innerHTML = "";

    // Open the table
    var additional_div_text  = `
    <table>
        <tr>
            <th>Chip Models</th>
            <th>Plate Models</th>
            <th>Syringe Models</th>
        </tr>
    `;

    // Add rows to the table
    for (var row=0; row<table_rows; row++) {
        // Open row
        additional_div_text += `<tr>`
        // Add data to row
        for (var col=0; col<3; col++) {
            var table_data;
            switch (col) {
                case 0:
                    // Add chip model
                    table_data = chips_list[row];
                    break;
                case 1:
                    // Add plate model
                    table_data = plates_list[row];
                    break;
                case 2:
                    // Add syringe model
                    table_data = syringes_list[row];
                    break;
            }
            if (table_data == undefined) {
                table_data = "";
            }
            additional_div_text += `<td>${table_data}</td>`
        }
        // Close row
        additional_div_text += `</tr>`
    }

    // Close the table
    additional_div_text += `</table>`;

    models_table_div.insertAdjacentHTML("afterbegin", additional_div_text);
}

function reset_model_lists() {
    models_table_div.innerHTML = '';
}

function toggle_visibility(visible_category){
    if (visible_category == "chips"){
        // Make chip properties input visible
        chip_properties_div.hidden = false;
        plate_properties_div.hidden = true;
        syringe_properties_div.hidden = true;
    }
    else if (visible_category == "plates"){
        // Make plate properties input visible
        chip_properties_div.hidden = true;
        plate_properties_div.hidden = false;
        syringe_properties_div.hidden = true;
    }
    else if (visible_category == "syringes"){
        // Make syringe properties input visible
        chip_properties_div.hidden = true;
        plate_properties_div.hidden = true;
        syringe_properties_div.hidden = false;
    }
}

// ----------------------- EVENT LISTENER METHODS

chip_radio_input.onclick = function() {
    toggle_visibility("chips");
}

plate_radio_input.onclick = function() {
    toggle_visibility("plates");
}

syringe_radio_input.onclick = function() {
    toggle_visibility("syringes");
}

chip_grid_rows.oninput = function() {
    check_chip_grid_inputs();
}

chip_grid_columns.oninput = function() {
    check_chip_grid_inputs();
}

plate_grid_rows.oninput = function() {
    check_plate_grid_inputs();
}

plate_grid_columns.oninput = function() {
    check_plate_grid_inputs();
}

confirm_parameters_btn.onclick = function() {
    final_new_model_properties = extract_all_inputs();

    if (final_new_model_properties != false) {
        // Write User Summary Section
        write_user_summary(final_new_model_properties);

        // Hide the input divs
        user_inputs_div.hidden = true;

        // Show the summary div
        user_summary_div.hidden = false;

        // Show the go to edit mode button
        back_to_edit_mode_btn.hidden = false;

        // Enable create model button
        create_model_btn.disabled = false;

        // Hide confirm parameters button
        confirm_parameters_btn.hidden = true;

        // Show confirmation feedback message
        confirmation_feedback_div.innerHTML = "<h3>VERIFY all the properties, then PRESS 'Create Model!'</h3>"
    }
    else {
        console.log("NOTHING TO CONFIRM. SOME MODEL PARAMETERS ARE EMPTY");
        // Show confirmation feedback message 
        confirmation_feedback_div.innerHTML = '<h3 style=color:red;">Some required fields were left blank, cannot confirm <h3>'
        
    }
}

back_to_edit_mode_btn.onclick = function() {
    // Reset confirmation feedback message
    confirmation_feedback_div.innerHTML = "<br>"

    // Show confirm parameters button
    confirm_parameters_btn.hidden = false;

    // Disable create model button
    create_model_btn.disabled = true;

    // Hide go to edit mode button
    back_to_edit_mode_btn.hidden = true;

    // Hide summary div
    user_summary_div.hidden = true;
    
    // Show input divs
    user_inputs_div.hidden = false;

    // Empty User Summary section
    user_summary_div.innerHTML = ``;
}

create_model_btn.onclick = function() {
    console.log("NEW MODEL", final_new_model_properties);
    // Send properties of new model to the server
    socket.emit("new_labware_model", final_new_model_properties);
    // Reset confirmation feedback message
    alert("Model created and registered in the server!");
    // Reload the create labware page
    window.location.reload();
}