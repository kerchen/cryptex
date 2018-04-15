% rebase('base.tpl', title=title)
% import shared_cfg
<p>Entries</p>
<ul>
    % for k, e in shared_cfg.pw_store.get_entries_by_path(path):
        <li>{{k}}</li>
    % end
</ul>
<p>Folders</p>
<ul>
    % for k, c in shared_cfg.pw_store.get_containers_by_path(path):
    <li>{{k}}</li>
    % end
</ul>

<form action="/manage" method="post">
    <input type="submit" name="addentry" value="Add Entry">
    <input type="submit" name="addcontainer" value="Add Folder">
</form>
