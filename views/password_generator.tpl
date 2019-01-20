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
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">Header</h4>
            </div>
            <div class="modal-body">
                % include(generated_template_filename)
            </div>
            <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Yes</button>
                <button type="button" class="btn" data-dismiss="modal">No</button>
            </div>
        </div>
    </div>
</div>

<script src="js/cryptex.js"></script>
<script src="js/seedrandom.js"></script>
<script>
function generatePassword() {
    var modal = document.getElementById('password-gen-modal');
//    modal.getElementsByTagName("button")[0].setAttribute("onclick", onConfirmFunction);
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

    var previewText = document.getElementById('generated-password-text');
    Math.seedrandom();
    var pwd = ""
    var desired_len = 20;
    for ( var i = 0; i < desired_len; i++) {
        var idx = Math.floor(Math.random() * charSet.length);
        pwd += charSet[idx];
    }
    previewText.innerHTML = encodeHTML(pwd);
}
</script>
<!--
