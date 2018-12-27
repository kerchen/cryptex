-->
% import shared_cfg
% import path_util
% encoded_path = path_util.encode_path(path)
% for k, _ in shared_cfg.get_containers_by_path(path):
<br>
    % if encoded_path == '+':
        <a class="link-text entry-link" href="/manage{{encoded_path}}{{k}}">{{k}}</a>
    % else:
        <a class="link-text entry-link" href="/manage{{encoded_path}}+{{k}}">{{k}}</a>
    % end
</br>
% end
% for k, _ in shared_cfg.get_entries_by_path(path):
<br>
    % if encoded_path == '+':
        <a class="link-text entry-link" href="/manage{{encoded_path}}{{k}}">{{k}}</a>
    % else:
        <a class="link-text entry-link" href="/manage{{encoded_path}}+{{k}}">{{k}}</a>
    % end
</br>
% end
<!--