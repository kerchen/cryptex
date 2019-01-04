-->
<div class="modal fade" id="confirm-modal" role="dialog">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">Header</h4>
            </div>
            <div class="modal-body">
                <p>Body</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Yes</button>
                <button type="button" class="btn" data-dismiss="modal">No</button>
            </div>
        </div>
    </div>
</div>

<script>
function confirmAction(header, body, onConfirmFunction) {
    var modal = document.getElementById('confirm-modal'); //$('#confirm-modal');
    modal.getElementsByClassName('modal-header')[0].innerHTML = header;
    modal.getElementsByClassName('modal-body')[0].innerHTML = body;
    modal.getElementsByTagName("button")[0].setAttribute("onclick", onConfirmFunction);
    $('#confirm-modal').modal('show');
}
</script>
<!--