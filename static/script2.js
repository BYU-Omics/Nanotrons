function addRow() {

    var myName = document.getElementById("name");
    var age = document.getElementById("age");
    var table = document.getElementById("myTableData");
 
    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);
 
    row.insertCell(0).innerHTML= '<input type="button" value = "Delete" onClick="Javacsript:deleteRow(this)">';
    row.insertCell(1).innerHTML= myName.value;
    row.insertCell(2).innerHTML= age.value;
 
}
 
function deleteRow(obj) {
      
    var index = obj.parentNode.parentNode.rowIndex;
    var table = document.getElementById("myTableData");
    table.deleteRow(index);
    
}
 
function addTable() {
      
    var myTableDiv = document.getElementById("myDynamicTable");
      
    var table = document.createElement('TABLE');
    table.border='1';
    
    var tableBody = document.createElement('TBODY');
    table.appendChild(tableBody);
    

    const fs = require('fs');

    // read JSON object from file
    fs.readFile('../scripts/qc.json', 'utf-8', (err, data) => {
        if (err) {
            throw err;
        }

        // parse JSON object
        const user = JSON.parse(data.toString());

        // print JSON object
        console.log(user);
    });


    for (var i=0; i<3; i++){
       var tr = document.createElement('TR');
       tableBody.appendChild(tr);
       
       for (var j=0; j<4; j++){
           var td = document.createElement('TD');
           td.width='75';
           td.appendChild(document.createTextNode("jacob"));
           tr.appendChild(td);
       }
    }
    myTableDiv.appendChild(table);
    
}
 
function load() {
    
    console.log("Page load finished");
 
}


This page needs:
        1. Start with choose script or create/upload script options
            a. Choose script allows you to pick a script that already exists
                i. a drop down menu to select the script you want to run
            b. Create new script takes you to the page which can do two things
                i. you can upload a new json file that is already written
                ii. use the gui to create and save the new json file. Once saved
                    you go back and click the choose script button and it should be
                    on the updated list
        2. After selecting a script, a button pops up that allows you to make a batch
        3. After both those are complete, you can then click the run batch button
            a. this will let you know if there are any errors
            b. a pop up will ask you if "this will take x hours and y minutes. Is this okay?"
            c. if you click yes then a pop up will ask "is the first sample wet or dry?"
            d. then the batch will start
