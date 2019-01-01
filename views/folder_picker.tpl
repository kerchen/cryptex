-->
% import shared_cfg
<ul id="cryptexTreeView">
    % include('subfolder_tree.tpl', level_name="(Root)", level="/", exclude_path=exclude_path)
</ul>
<script>
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".nested").classList.toggle("active");
        this.classList.toggle("caret-down");
    });
}

function switchLevel(level) {
    var selection_label = document.getElementById("{{selection_display_id}}");
    selection_label.innerHTML = level;
}
</script>

<!--
