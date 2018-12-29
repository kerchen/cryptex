-->
% import shared_cfg
% import path_util
% encoded_path = path_util.encode_path(path)
% if shared_cfg.get_entry_count_by_path(path) > 0:
    <span class="text-element contents-label">entries</span>
    <table style="width:100%">
    % for k, _ in shared_cfg.get_entries_by_path(path):
        % if encoded_path == '+':
            % item_path = encoded_path + k
        % else:
            % item_path = encoded_path + "+" + k
        % end
        <tr>
            <td style="width:5%">
                <button type="button" class="btn manage-store-btn" formmethod="post" onclick="deleteEntry('{{item_path}}')">X</button>
            </td>
            <td style="width:5%">
                <button type="button" class="btn manage-store-btn" formmethod="post" onclick="editEntry('{{item_path}}')">E</button>
            </td>
            <td>
                <span class="text-element list-entry">{{k}}</span>
            </td>
        </tr>
    % end
    </table>
% end
<!--