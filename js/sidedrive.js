var _counter = 0;
function gimme_unique_id() {
    return _counter++;
}

function submit_action() {
    // Action for the submit button

    // 1) Add a new file icon.
    var id = gimme_unique_id();
    var newFile = $("<div id='draggable" + id + "'><span class='glyphicon glyphicon-file'></span></div>");
    newFile.attr("fileId", id);
    $("#file-container").append(newFile);
    newFile.draggable({revert: "invalid", axis: "curve"});

    // 2) Stage the file information
    var key = $("#key").val();
    var value = $("#value").val();
    store_local_file(id, key, value);

    // 3) Reset the form
    $("#key").val("");
    $("#value").val("");
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
