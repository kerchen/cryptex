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


function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue + ";path=/";
}


function deleteCookie(cname) {
    document.cookie = cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}


function getCookiesWithPrefix(prefix) {
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  var matches = [];
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(prefix) == 0) {
      key_value = c.split('=');
      matches.push(key_value[0]);
    }
  }
  return matches;
}


function loginCommit() {
    // Uses the entered password to try to log in.
    var password = document.getElementById("password-store-pw").value;

    post('/login', {password: password});
}


function createStoreCommit() {
    // Requests an empty master store to be created, encrypted with the entered
    // passwords.
    var pw1 = document.getElementById("password-store-pw").value;
    var pw2 = document.getElementById("password-store-pw2").value;

    post('/create-store', {password: pw1, password_confirm: pw2});
}


function manageShowSessionPath() {
    // Returns to the management page, showing the current session path.
    post('/manage-command', {action: 'show-session-path'});
}


function updateMasterPasswordCommit() {
    // Updates the master password, using the entered passwords.
    var currentPass = document.getElementById("password-current").value;
    var newPass = document.getElementById("password-new").value;
    var newPassReenter = document.getElementById("password-new-reenter").value;

    post('/change-master-password',
         {new_password: newPass,
          new_password_confirm: newPassReenter,
          current_password: currentPass});
}


function createFolder(encodedParentPath) {
    // Causes a transition to the create-folder page.
    post('/manage-command', {action: 'create-folder', encoded_parent_path: encodedParentPath});
}


function editFolder(encodedPath) {
    // Causes a transition to the edit-folder page.
    post('/manage-command', {action: 'edit-folder', encoded_path: encodedPath});
}


function moveFolder(encodedPath) {
    // Causes a transition to the move-folder page.
    post('/manage-command', {action: 'move-folder', encoded_path: encodedPath});
}


function deleteFolder(encodedPath) {
    // Causes a transition to the delete-folder page.
    post('/manage-command', {action: 'delete-folder', encoded_path: encodedPath});
}


function createFolderCommit() {
    // Causes a new folder to be created, named according to what the user entered.
    var folderName = document.getElementById("folder-name-input").value;

    post('/manage-new-container', {name: folderName});
}


function editFolderCommit() {
    // Causes a folder to be updated using data from fields in the edit-folder page.
    // Note that the current folder name is stashed in the element that displays
    // the current name, using a custom attribute named 'data-current-folder-name'.
    var currentFolderName = document.getElementById("current-folder-name-text").getAttribute("data-current-folder-name");
    var newFolderName = document.getElementById("folder-name-input").value;

    post('/manage-edit-folder',
         {current_folder_name: currentFolderName,
          new_folder_name: newFolderName});
}


function moveFolderCommit() {
    // Causes a folder to be moved using data from the move-folder page.
    var itemPath = document.getElementById("item-path-text").innerHTML;
    var destinationPath = document.getElementById("destination-path-text").innerHTML;

    post('/manage-move-folder', {item_path: itemPath, destination_path: destinationPath});
}


function deleteFolderCommit(folderPath) {
    // Causes a folder to be deleted using data from the delete-folder page.
    post('/manage-delete-folder', {folder_path: folderPath});
}


function createEntry(encodedParentPath) {
    // Causes a transition to the create-entry page.
    post('/manage-command', {action: 'create-entry', encoded_parent_path: encodedParentPath});
}


function editEntry(encodedPath) {
    // Causes a transition to the edit-entry page.
    post('/manage-command', {action: 'edit-entry', encoded_path: encodedPath});
}


function moveEntry(encodedPath) {
    // Causes a transition to the move-entry page.
    post('/manage-command', {action: 'move-entry', encoded_path: encodedPath});
}


function deleteEntry(encodedPath) {
    // Causes a transition to the delete-entry page.
    post('/manage-command', {action: 'delete-entry', encoded_path: encodedPath});
}


function createEntryCommit() {
    // Causes an Entry to be created using data from fields in the
    // create-entry page.
    var entryName = document.getElementById("entry-name-input").value;
    var userName = document.getElementById("user-name-input").value;
    var password1 = document.getElementById("password-input").value;
    var password2 = document.getElementById("password-confirm-input").value;
    var url = document.getElementById("url-input").value;

    post('/manage-create-entry',
         {entryname: entryName,
          username: userName,
          password1: password1,
          password2: password2,
          url: url});
}


function editEntryCommit() {
    // Causes an Entry to be updated using data from fields in the edit-entry page.
    // Note that the current entry name is stashed in the element that displays
    // the current name, using a custom attribute named 'data-current-entry-name'.
    var currentEntryName = document.getElementById("current-entry-name-text").getAttribute("data-current-entry-name");
    var entryName = document.getElementById("entry-name-input").value;
    var userName = document.getElementById("user-name-input").value;
    var password1 = document.getElementById("password-input").value;
    var password2 = document.getElementById("password-confirm-input").value;
    var url = document.getElementById("url-input").value;

    post('/manage-edit-entry',
         {current_entry_name: currentEntryName,
          entryname: entryName,
          username: userName,
          password1: password1,
          password2: password2,
          url: url});
}


function moveEntryCommit() {
    // Causes an entry to be moved according to data entered in the move-entry page.
    var itemPath = document.getElementById("item-path-text").innerHTML;
    var destinationPath = document.getElementById("destination-path-text").innerHTML;

    post('/manage-move-entry', {item_path: itemPath, destination_path: destinationPath});
}


function deleteEntryCommit(entryPath) {
    // Causes an Entry to be deleted using data from the delete-entry page.
    post('/manage-delete-entry', {entry_path: entryPath});
}


