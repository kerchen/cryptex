-->
% import shared_cfg
% folders = path.split("/")
% accum_path = ""
% for f in folders:
    % if len(f):
        % if len(accum_path) > 0:
            % accum_path += "+"
        % end
        % accum_path += f
    % end
% end
<ul>
% for k, c in shared_cfg.get_containers_by_path(path):
    % if len(accum_path) > 0:
        <li><a class="link-text entry-link" href="/manage={{accum_path}}+{{k}}">{{k}}</a></li>
    % else:
        <li><a class="link-text entry-link" href="/manage={{k}}">{{k}}</a></li>
    % end
    <ul>
    %   for k1, c1 in c.get_containers():
        % if len(accum_path) > 0:
            <li><a class="link-text entry-link" href="/manage={{accum_path}}+{{k}}+{{k1}}">{{k1}}</a></li>
        % else:
            <li><a class="link-text entry-link" href="/manage={{k}}+{{k1}}">{{k1}}</a></li>
        %end
    %   end
    </ul>
% end
</ul>
<!--