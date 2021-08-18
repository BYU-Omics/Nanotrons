/* Made by @fitri
	This is a component of my ReactJS project
	https://codepen.io/fitri/full/oWovYj/ 
	Adapted by Sebastian Zapata and Alejandro Brozalez
*/

var add_element_btn = document.getElementById("add_element");
var log_current_list_btn = document.getElementById("log_current_list");
var batch_elements_list = document.getElementById("batch_elements_list");


// --------------------------- DEBUGGING METHODS ---------------------------

log_current_list_btn.onclick =  function() {
	var current_list = convert_ul_to_list(batch_elements_list);
	console.log("current_list", current_list);
}

function convert_ul_to_list(ul_element) {
	var ul_items = ul_element.getElementsByTagName("li");
	var list_items = [];
	for (var i=0; i < ul_items.length; i++) {
		list_items.push(ul_items[i].innerText.split("\n"));
	}
	return list_items
}

add_element_btn.onclick = function() {

}

// --------------------------- DRAG AND DROP METHODS ---------------------------

function enableDragSort(listClass) {
	const sortableLists = document.getElementsByClassName(listClass);
	Array.prototype.map.call(sortableLists, (list) => {enableDragList(list)});
}

function enableDragList(list) {
	Array.prototype.map.call(list.children, (item) => {enableDragItem(item)});
}

function enableDragItem(item) {
	item.setAttribute('draggable', true)
	item.ondrag = handleDrag;
	item.ondragend = handleDrop;
}

function handleDrag(item) {
	const selectedItem = item.target;
	list = selectedItem.parentNode;
	x = event.clientX;
	y = event.clientY;

	selectedItem.classList.add('drag-sort-active');
	let swapItem = document.elementFromPoint(x, y) === null ? selectedItem : document.elementFromPoint(x, y);

	if (list === swapItem.parentNode) {
		swapItem = swapItem !== selectedItem.nextSibling ? swapItem : swapItem.nextSibling;
		list.insertBefore(selectedItem, swapItem);
	}
}

function handleDrop(item) {
	item.target.classList.remove('drag-sort-active');
}

(()=> {enableDragSort('drag-sort-enable')})();

// --------------------------- SORTING ALGORITHM METHODS ---------------------------


// --------------------------- LOAD GROUP METHODS ---------------------------

let divElement = document.createElement('div')

let textNode = document.createTextNode('This is newly created element')

divElement.appendChild(textNode)

let containerDiv = document.querySelector('.container')

containerDiv.appendChild(divElement)

// --------------------------- DELETE SAMPLE METHODS --------------------------- 
/*
Here there will be methods that assign the id to each trash can image in accordance with the index of the list element that they belong to 
*/