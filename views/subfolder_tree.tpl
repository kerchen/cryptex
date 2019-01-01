
% if exclude_path and exclude_path == level:
    <li>{{level_name}}</li>
% else:
    % folders = shared_cfg.get_containers_by_path(level)
    % if len(folders):
        <li><span class="caret">
                <a class="a link-text path-component-link" onclick="switchLevel('{{level}}')" >{{level_name}}</a>
            </span>
            <ul class="nested">
                % for f, _ in folders:
                    % if level.endswith("/"):
                        % include('subfolder_tree.tpl', level_name=f, level=level+f)
                    % else:
                        % include('subfolder_tree.tpl', level_name=f, level=level+'/'+f)
                    % end
                % end
            </ul>
        </li>
    % else:
        <li>
            <a class="a link-text path-component-link" onclick="switchLevel('{{level}}')" >{{level_name}}</a>
        </li>
    % end
%end
