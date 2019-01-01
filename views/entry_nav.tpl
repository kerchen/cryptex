-->
% import shared_cfg
% import path_util
% encoded_path = path_util.encode_path(path)
% if shared_cfg.get_entry_count_by_path(path) > 0:
    <table style="width:100%">
    % for k, _ in shared_cfg.get_entries_by_path(path):
        % if encoded_path == '+':
            % entry_path = encoded_path + k
        % else:
            % entry_path = encoded_path + "+" + k
        % end
        <tr>
            <td width="5%">
                <button type="button" class="btn icon-btn delete-item-btn" formmethod="post" onclick="deleteEntry('{{entry_path}}')"></button>
            </td>
            <td width="5%">
                <button type="button" class="btn icon-btn edit-item-btn" formmethod="post" onclick="editEntry('{{entry_path}}')"></button>
            </td>
            <td style="width:5%">
                <button type="button" class="btn icon-btn move-item-btn" formmethod="post" onclick="moveFolder('{{entry_path}}')"></button>
            </td>
            <td>
                <span class="text-element list-entry">{{k}}</span>
            </td>
        </tr>
    % end
    </table>
% else:
    <span class="text-element manage-label manage-msg">This folder doesn't have any entries. You can click on the '+' button to add some.</span>
% end
<!--