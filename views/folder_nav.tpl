-->
% import shared_cfg
% import path_util
% encoded_path = path_util.encode_path(path)
<style>
th, td {
  padding: 4px;
}
</style>
% if shared_cfg.get_container_count_by_path(path) > 0:
    <table style="width:100%">
    % for k, _ in shared_cfg.get_containers_by_path(path):
        % if encoded_path == '+':
            % item_path = encoded_path + k
        % else:
            % item_path = encoded_path + "+" + k
        % end
        <tr>
            <td style="width:5%">
                <button type="button" class="btn icon-btn delete-item-btn" formmethod="post" onclick="deleteFolder('{{item_path}}')"></button>
            </td>
            <td style="width:5%">
                <button type="button" class="btn icon-btn edit-item-btn" formmethod="post" onclick="editFolder('{{item_path}}')"></button>
            </td>
            <td style="width:5%">
                <button type="button" class="btn icon-btn move-item-btn" formmethod="post" onclick="moveFolder('{{item_path}}')"></button>
            </td>
            <td>
                <a class="a link-text path-component-link" href="/manage{{item_path}}">{{k}}</a>
            </td>
        </tr>
    % end
    </table>
% else:
    <span class="text-element manage-label manage-msg">This folder doesn't have any sub-folders. You can click on the '+' button to add some.</span>
% end
<!--