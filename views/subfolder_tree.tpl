% # This template expects this variables:
% # level: A string holding the full path to the level to be added to the tree.
% # level_name: A string holding the display name of the level. Usually this is just
% #             the name of the folder.
% # exclude_path: A string indicating a path which should not be made traversed
% #             further nor made expandable. Set to None to disable this behavior.
% # show_entries: A boolean indicating whether or not entries should be shown in
% #             the tree.
% # use_dropdowns: A boolean indicating whether or not items in the tree should
% #             display dropdown menus when clicked. If false, the default 'onclick'
% #             behavior will be used (which is to invoke the switchLevel() function
% #             for folders and do nothing for entries).

% from hashlib import sha1
% import path_util
% if exclude_path and exclude_path == level:
    <li>
        <span style="display:inline-block; width: 22px;"></span>
        <text class="read-only-value-text">{{level_name}}</text>
    </li>
% else:
    % folders = shared_cfg.get_containers_by_path(level)
    % item_count = len(folders)
    % show_move = True
    % if level == "/" and item_count == 0:
        % show_move = False
    % end
    % if show_entries:
        % entries = shared_cfg.get_entries_by_path(level)
        % item_count += len(entries)
    % else:
        % entries = []
    % end
    % folder_drop_items = None
    % entry_drop_items = None
    % if use_dropdowns:
        % encoded_folder_path = path_util.encode_path(level)
        % folder_drop_items = [
        %   ("create entry", "createEntry", "{0}".format(encoded_folder_path)),
        %   ("create sub-folder", "createFolder", "{0}".format(encoded_folder_path)) ]
        % if level != "/":
            % folder_drop_items.append(("move folder", "moveFolder", "{0}".format(encoded_folder_path)))
            % folder_drop_items.append(("edit folder", "editFolder", "{0}".format(encoded_folder_path)))
            % folder_drop_items.append(("delete folder", "deleteFolder", "{0}".format(encoded_folder_path)))
        % end
    % end
    % if item_count > 0:
        <li><span class="caret"></span>
        % if use_dropdowns:
            % dropdown_id = "fdd{0}".format(sha1(encoded_folder_path).hexdigest())
            % include('dropdown.tpl',
            %         item_text=level_name,
            %         item_type='folder',
            %         dropdown_id=dropdown_id,
            %         dropdown_items=folder_drop_items)
        % else:
            <a class="link-button tree-folder-link-btn" onclick="switchLevel('{{level}}')" >{{level_name}}</a>
        % end
        <ul class="nested">
        % for f, _ in folders:
            % if level.endswith("/"):
                % include('subfolder_tree.tpl', level_name=f, level=level+f)
            % else:
                % include('subfolder_tree.tpl', level_name=f, level=level+'/'+f)
            % end
        % end
        % for e, _ in entries:
            <li>
                <span style="display:inline-block; width: 12px;"></span>
            % if use_dropdowns:
                % encoded_entry_path = path_util.encode_path(level + "/" + e)
                % entry_drop_items = [ ]
                % if show_move:
                    % entry_drop_items.append(("move entry", "moveEntry", "{0}".format(encoded_entry_path)))
                % end
                % entry_drop_items.append(("edit entry", "editEntry", "{0}".format(encoded_entry_path)))
                % entry_drop_items.append(("delete entry", "deleteEntry", "{0}".format(encoded_entry_path)))

                % dropdown_id = "edd{0}".format(sha1(encoded_entry_path).hexdigest())
                % include('dropdown.tpl',
                %         item_text=e,
                %         item_type='entry',
                %         dropdown_id=dropdown_id,
                %         dropdown_items=entry_drop_items)
            % else:
                <a class="link-button tree-entry-link-btn" onclick="selectEntry('{{level}}', '{{e}}')" >{{e}}</a>
            % end
            </li>
        % end
        </ul>
        </li>
    % else:
        <li>
            <span style="display:inline-block; width: 12px;"></span>
        % if use_dropdowns:
            % dropdown_id = "fdd{0}".format(sha1(encoded_folder_path).hexdigest())
            % include('dropdown.tpl',
            %         item_text=level_name,
            %         item_type='folder',
            %         dropdown_id=dropdown_id,
            %         dropdown_items=folder_drop_items)
        % else:
                <a class="link-button tree-folder-link-btn" onclick="switchLevel('{{level}}')" >{{level_name}}</a>
        % end
        </li>
    % end
%end

