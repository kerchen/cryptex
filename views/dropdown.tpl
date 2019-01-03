% # This template expects these variables:
% #   item_text: A string that will be shown for the item.
% #   item_type: Indicates what type of item this dropdown is for. Can be either
% #                'entry' or 'folder' (case matters!).
% #   dropdown_id: A string which will be used as a Javascript ID that uniquely
% #                identifies this dropdown instance.
% #   dropdown_items: Iterable of tuples. Each tuple defines an item in the dropdown,
% #                with the first element being the text of the item and the second a
% #                string which will be assigned to the 'onclick' attribute.

<div class="dropdown">
    <a class="dropbtn link-button tree-{{item_type}}-link-btn" data-dropdown-id="{{dropdown_id}}" onclick="toggleMenu('{{dropdown_id}}')" >{{item_text}}</a>
    <div id="{{dropdown_id}}" class="dropdown-content">
        % for i in dropdown_items:
            <button class="dropdown-btn" onclick="{{i[1]}}('{{i[2]}}')">{{i[0]}}</button>
        % end
    </div>
</div>
