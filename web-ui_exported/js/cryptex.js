
function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


// Sets the ID of the button that should be clicked when return is pressed in
// a text entry element.
function setReturnButton(textElementID, buttonID) {
    var textElement = document.getElementById(textElementID);

    textElement.addEventListener("keydown",
        function(event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                document.getElementById(buttonID).click();
            }
        }
    );
}


// Sets the value of a text input control, converting from HTML.
function setHTMLInputValue(id, value) {
  if (value) {
      document.getElementById(id).value = jQuery.parseHTML(value)[0].textContent;
  } else {
      document.getElementById(id).value = "";
  }
}


function login() {
    var password = document.getElementById("password-store-pw").value;

    post('/login', {password: password});
}



function createStore() {
    var pw1 = document.getElementById("password-store-pw").value;
    var pw2 = document.getElementById("password-store-pw2").value;

    post('/create-store', {password: pw1, password_confirm: pw2});
}


function manageShowSessionPath() {
    // Returns to the management page, showing the current session path.
    post('/manage', {action: 'showsessionpath'});
}


function updateMasterPassword() {
    var currentPass = document.getElementById("password-current").value;
    var newPass = document.getElementById("password-new").value;
    var newPassReenter = document.getElementById("password-new-reenter").value;

    post('/change-master-password',
         {new_password: newPass,
          new_password_confirm: newPassReenter,
          current_password: currentPass});
}

function addFolder() {
    // Causes transition to folder name entry interface
    post('/manage', {action: 'addcontainer'});
}


function createFolder() {
    var folderName = document.getElementById("folder-name-input").value;

    post('/manage-new-container', {name: folderName});
}


function deleteFolder(path) {
    if (confirm("Delete this folder and all of the entries it contains?\n"+path)) {
        alert("Not implemented yet.");
        //post('/remove-container',
             //{encoded_path: path});
    }
}

function editFolder(path) {
    //if (confirm("Delete this folder and all of the entries it contains?\n"+path)) {
        alert("Not implemented yet.");
        //post('/remove-container',
             //{encoded_path: path});
    //}
}

function addEntry() {
    // Causes transition to Entry data input interface
    post('/manage', {action: 'addentry'});
}

function editEntry(itemPath) {
    // Causes transition to Entry data edit interface
    post('/manage', {action: 'editentry', item_path: itemPath});
}

function createEntry() {
    var entryName = document.getElementById("entry-name-input").value;
    var userName = document.getElementById("user-name-input").value;
    var password1 = document.getElementById("password-input").value;
    var password2 = document.getElementById("password-confirm-input").value;
    var url = document.getElementById("url-input").value;

    post('/manage-new-entry',
         {entryname: entryName,
          username: userName,
          password1: password1,
          password2: password2,
          url: url});
}

function updateEntry() {
    var currentEntryName = document.getElementById("current-entry-name-text").getAttribute("data-original-entry-name");
    var entryName = document.getElementById("entry-name-input").value;
    var userName = document.getElementById("user-name-input").value;
    var password1 = document.getElementById("password-input").value;
    var password2 = document.getElementById("password-confirm-input").value;
    var url = document.getElementById("url-input").value;

    post('/manage-update-entry',
         {current_entry_name: currentEntryName,
          entryname: entryName,
          username: userName,
          password1: password1,
          password2: password2,
          url: url});
}

