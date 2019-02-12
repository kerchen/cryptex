
function togglePasswordVisibility() {
    var pwd_input = document.getElementById("password-input");
    var pwd_confirm_input = document.getElementById("password-confirm-input");

    if ( pwd_input.type === "password" ) {
        pwd_input.type = "text";
        pwd_input.className = "form-input";
        pwd_confirm_input.type = "text";
        pwd_confirm_input.className = "form-input";
    } else {
        pwd_input.type = "password";
        pwd_input.className = "form-password-input";
        pwd_confirm_input.type = "password";
        pwd_confirm_input.className = "form-password-input";
    }
}