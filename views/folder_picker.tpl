% # This template expects this variables:
% # exclude_path: A string indicating a path which should not be made traversed
% #             further nor made expandable. Set to None to disable this behavior.
% # show_entries: A boolean indicating whether or not entries should be shown in
% #             the tree.
% # use_dropdowns: A boolean indicating whether or not items in the tree should
% #             display dropdown menus when clicked. If false, the default 'onclick'
% #             behavior will be used (which is to invoke the switchLevel() function
% #             for folders and do nothing for entries).
% # selection_display_id: Only used when there are no dropdowns. This string is
% #             used by the switchLevel() function to know which text element
% #             to update whenever the function is called.
% # remember_state: A boolean indicating whether or not the tree control should
% #             use cookie values to save its state.
-->
% import shared_cfg
<ul id="cryptexTreeView">
    % include('subfolder_tree.tpl', level_name="/ (root)", level="/",
    %         exclude_path=exclude_path, show_entries=show_entries,
    %         use_dropdowns=use_dropdowns,
    %         hash_salt=(shared_cfg.session.key if remember_state else None))
</ul>
<script>
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".nested").classList.toggle("active");
        if (this.hasAttribute("id")) {
            if (this.classList.toggle("caret-down")) {
                setCookie(this.getAttribute("id"), "1");
            } else {
                deleteCookie(this.getAttribute("id"));
            }
        } else {
            this.classList.toggle("caret-down");
        }
    });
}

var expander = document.getElementsByClassName("caret");
var expandedNodes = getCookiesWithPrefix("tn");
for (i = 0; i < expander.length; i++) {
    var id = expander[i].getAttribute("id");
    if (id == "root") {
        expander[i].click();
    } else if ( id ) {
        var j;
        for (j = 0; j < expandedNodes.length; j++) {
            if (expandedNodes[j] == id) {
                expander[i].click();
                break;
            }
        }
    }
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
