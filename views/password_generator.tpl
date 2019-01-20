-->
% # Use the body of the RBB-created password generator page as the guts of the
% # password generator dialog.
% import server
% generated_template_filename = server.generate_template_from_body('password-generator-popup.html')
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
<script>
function generatePassword() {
    var modal = document.getElementById('password-gen-modal');
//    modal.getElementsByTagName("button")[0].setAttribute("onclick", onConfirmFunction);
    $('#password-gen-modal').modal('show');
}

function generatePreview() {
    var previewText = document.getElementById('generated-password-text');
    previewText.innerHTML = encodeHTML('hi&h<&amp;123][{>!');
}
</script>
<!--
