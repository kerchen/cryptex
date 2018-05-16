% rebase('base.tpl', title=title)
% import shared_cfg
<a href="/manage/">Root</a>
% folders = path.split("/")
% accum_path = ""
% for f in folders:
    % if len(f):
        % accum_path = accum_path + "/" + f
        <a href="/manage{{accum_path}}">/{{f}}</a>
    % end
% end
<p>Folders</p>
<ul>
    % for k, c in shared_cfg.get_containers_by_path(path):
    % if path == "/":
        <li><a href="/manage/{{k}}">{{k}}</a></li>
    % else:
        <li><a href="/manage{{path}}/{{k}}">{{k}}</a></li>
    % end
    % end
</ul>
<p>Entries</p>
<ul>
    % for k, e in shared_cfg.get_entries_by_path(path):
    <li>{{k}}</li>
    % end
</ul>

<form action="/manage" method="post">
    <input type="submit" path="{{path}}" name="addentry" value="Add Entry">
    <input type="submit" path="{{path}}" name="removeentry" value="Remove Entry">
    <input type="submit" path="{{path}}" name="addcontainer" value="Add Folder">
    <input type="submit" path="{{path}}" name="removecontainer" value="Remove Folder">
</form>
<br/>
