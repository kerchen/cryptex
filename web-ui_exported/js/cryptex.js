
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


function login() {
    var password = document.getElementById("password-store-pw").value;

    if (password.length < 1) {
        alert("Password cannot be empty.")
        return
    }

    post('/login', {password: password});
}


function lock() {
    post('/lock', {});
}


function changeMasterPassword() {
    post('/master-pass', {});
}


function manageStore() {
    post('/manage', {});
}


function activate() {
    post('/activate', {});
}



function createStore() {
    var pw1 = document.getElementById("password-store-pw").value;
    var pw2 = document.getElementById("password-store-pw2").value;

    if (pw1.length < 1) {
        alert("Password cannot be empty.")
        return
    }

    if (pw1 != pw2) {
        alert("Entered passwords do not match. Please try again.")
        return
    }

    post('/create-store', {password: pw1});
}


function updateMasterPassword() {
    var currentPass = document.getElementById("password-current").value;
    var newPass = document.getElementById("password-new").value;
    var newPassReenter = document.getElementById("password-new-reenter").value;

    if (newPass.length < 1) {
        alert("Password cannot be empty.")
        return
    }

    if (newPass != newPassReenter) {
        alert("New passwords do not match. Please try again.")
        return
    }

    post('/change-master-password', {password: newPass});
}

