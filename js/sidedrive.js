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
