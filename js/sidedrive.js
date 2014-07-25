var _counter = 0;
function gimme_unique_id() {
    return _counter++;
}

function submit_action() {
    // Action for the submit button

    var key = $("#input-key").val();
    var value = $("#input-value").val();

    // 1) Add a new file icon.
    var id = gimme_unique_id();
    var newFile = $("<div id='draggable" + id + "' class='file-thing'>" + key + "</div>");
    newFile.attr("fileId", id);
    $("#file-container").append(newFile);
    newFile.draggable({revert: "invalid",
		       axis: "curve",
		       start: function (e, i) {file_draggable_start_cb(e,i);},
		       stop: function(e,i) {file_draggable_stop_cb(e,i);}
		      });

    // 2) Stage the file information
    store_local_file(id, key, value);

    // 3) Reset the form
    $("#input-key").val("");
    $("#input-value").val("");

    // 4) And the button color.
    save.css('background-color', '#ccc');
}

function cloud_drop(draggable, id) {
    var f = get_local_file(id);
    // 1) animate it to hide

    // Make it so that it doesn't try and revert animate back
    draggable.draggable("option", "revert", false);
    draggable.hide("puff");

    // 2) Submit to the CLOUD (or alert as stub)
    $.post("/drive", { "title" : f["key"], "info" : f["value"] })
    //alert("key: " + f['key'] + " val: " + f['value']);
}

var _files = {};
function store_local_file(id, key, value) {
    _files[id] = {"key" : key, "value" : value};
}

function get_local_file(id) {
    return _files[id];
}

// cache lookups
var input_key;
var input_value;
var save;
function button_color_change () {
    // for the save button. It should be red if the form is valid
    // and blue otherwise. Valid means that the key and value input
    // fields both have values in them.
    var key_valid = input_key.val().trim().length > 0;
    var value_valid = input_value.val().trim().length > 0;
    if (key_valid && value_valid) {
	save.css('background-color', '#ef3e37');
    } else {
	save.css('background-color', '#ccc');
    }
}

function file_draggable_start_cb (event, ui) {
    // Turn the cloud to hover
    // It appears it wants relative from where the js is ran
    $("#cloud").css('background-image', "url('img/cloud_hover.png')");

    // We can't rely on css:hover selector cuz of the parabola drag (the mouse
    // drags off of the element). So set the hover state here.
    $(event.target).css('background', "#eb1c23 url('img/red-gripper.png') no-repeat");
}

function file_draggable_stop_cb (event, ui) {
    // Turn the cloud back to static
    // It appears it wants relative from where the js is ran
    $("#cloud").css('background-image', "url('img/cloud_static.png')");

    // We can't rely on css:hover selector cuz of the parabola drag (the mouse
    // drags off of the element). So set the hover state here.
    $(event.target).css('background', "#858585 url('img/gripper2.png') no-repeat");
}
