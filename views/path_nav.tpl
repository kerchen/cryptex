-->
% import shared_cfg
<a class="link-text entry-link" href="/manage">(Root)</a>
% folders = path.split("/")
% accum_path = ""
% for f in folders:
    % if len(f):
        % if len(accum_path) > 0:
            % accum_path += "+"
        % end
        % accum_path += f
/
<a class="link-text entry-link" href="/manage={{accum_path}}">{{f}}</a>
    % end
% end
<!--