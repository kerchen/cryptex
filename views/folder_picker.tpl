-->
% import shared_cfg
<ul id="cryptexTreeView">
    % include('subfolder_tree.tpl', level_name="/ (root)", level="/",
    %         exclude_path=exclude_path)
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

function toggleMenu(id) {
  document.getElementById(id).classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.id != event.target.getAttribute("data-dropdown-id") &&
          openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
}

</script>

<!--
