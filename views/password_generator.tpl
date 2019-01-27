-->
% # Use the body of the RBB-created password generator page as the guts of the
% # password generator dialog.
% import server, shared_cfg
% generated_template_filename = server.generate_template_from_body('password-generator-popup.html')
% punctuation_chars = " ".join(shared_cfg.PASSWORD_CHARS_PUNCTUATION)
% bracket_chars = " ".join(shared_cfg.PASSWORD_CHARS_BRACKETS)
% other_chars = " ".join(shared_cfg.PASSWORD_CHARS_OTHERS)
% other_chars_for_js = shared_cfg.PASSWORD_CHARS_OTHERS.replace("\\", "\\\\")
<div class="modal fade" id="password-gen-modal" role="dialog">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-body">
                % include(generated_template_filename)
            </div>
        </div>
    </div>
</div>

<script src="js/cryptex.js"></script>
<script src="js/seedrandom.js"></script>
<script>
function showPasswordGenerator(onAcceptAction) {
    var modal = document.getElementById('password-gen-modal');
    var getPasswordCode = "document.getElementById('generated-password-text').innerHTML";
    var acceptCode = onAcceptAction + "(" + getPasswordCode + ")";
    document.getElementById("accept-password-btn").setAttribute("onclick", acceptCode);
    document.getElementById("password-length-input").defaultValue = "15";
    document.getElementById("generated-password-text").innerHTML = "generated";
    $('#password-gen-modal').modal('show');
}


function isOptionChecked(id) {
    var cb = document.getElementById(id);
    if ( ! cb ) {
        console.log("Option with ID " + id + " not found.");
        return false;
    }
    return true == cb.childNodes[0].checked;
}


function generatePreview() {
    var upperCase = "{{shared_cfg.PASSWORD_CHARS_UPPER_CASE}}";
    var lowerCase = "{{shared_cfg.PASSWORD_CHARS_LOWER_CASE}}";
    var digits = "{{shared_cfg.PASSWORD_CHARS_DIGITS}}";
    var punctuation = "{{shared_cfg.PASSWORD_CHARS_PUNCTUATION}}";
    var brackets = decodeHTML("{{shared_cfg.PASSWORD_CHARS_BRACKETS}}");
    var others = decodeHTML("{{other_chars_for_js}}");
    var spaces = " ";
    var charSet = "";

    if (isOptionChecked('uppercase-checkbox')) {
        charSet += upperCase;
    }
    if (isOptionChecked('lowercase-checkbox')) {
        charSet += lowerCase;
    }
    if (isOptionChecked('digits-checkbox')) {
        charSet += digits;
    }
    if (isOptionChecked('punctuation-checkbox')) {
        charSet += punctuation;
    }
    if (isOptionChecked('brackets-checkbox')) {
        charSet += brackets;
    }
    if (isOptionChecked('spaces-checkbox')) {
        charSet += spaces;
    }
    if (isOptionChecked('others-checkbox')) {
        charSet += others;
    }
    var includeChars = document.getElementById('include-chars-input').value;
    for ( var i = 0; i < includeChars.length; i++ ) {
        if ( charSet.indexOf(includeChars[i]) == -1 ) {
            charSet += includeChars[i];
        }
    }
    var excludeChars = document.getElementById('exclude-chars-input').value;
    var tempCharSet = "";
    for ( var i = 0; i < charSet.length; i++ ) {
        if ( excludeChars.indexOf(charSet[i]) == -1 ) {
            tempCharSet += charSet[i];
        }
    }
    charSet = tempCharSet;
    var desired_len = document.getElementById("password-length-input").value;

    if ( charSet.length == 0 || ! desired_len || desired_len < 1 ) {
        // TODO: Input error handling
        return;
    }

    var previewText = document.getElementById('generated-password-text');
    Math.seedrandom();
    var pwd = ""
    for ( var i = 0; i < desired_len; i++) {
        var idx = Math.floor(Math.random() * charSet.length);
        pwd += charSet[idx];
    }
    previewText.innerHTML = encodeHTML(pwd);
}
</script>
<!--
