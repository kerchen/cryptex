-->
% import shared_cfg
% import path_util
% encoded_path = path_util.encode_path(path)
% if shared_cfg.get_container_count_by_path(path) > 0:
    <span class="text-element contents-label">subfolders</span>
    <table style="width:100%">
    % for k, _ in shared_cfg.get_containers_by_path(path):
        % if encoded_path == '+':
            % item_path = encoded_path + k
        % else:
            % item_path = encoded_path + "+" + k
        % end
        <tr>
            <td style="width:5%">
                <button type="button" class="btn manage-store-btn" formmethod="post" onclick="deleteFolder('{{item_path}}')">X</button>
            </td>
            <td style="width:5%">
                <button type="button" class="btn manage-store-btn" formmethod="post" onclick="editFolder('{{item_path}}')">E</button>
            </td>
            <td>
                <a class="link-text entry-link" href="/manage{{item_path}}">{{k}}</a>
            </td>
        </tr>
    % end
    </table>
% end
<!--