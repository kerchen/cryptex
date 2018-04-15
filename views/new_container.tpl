% rebase('base.tpl', title="New Folder")
<h1>Create new folder</h1>
<form action="/manage-new-container" method="post">
    % if retry:
    <p class="error">Entered folder name already exists. Please try again.</p>
    % end
    Name: <input name="name" type="text"/> </br>
    <input name="create" value="Create" type="submit" />
    <input name="cancel" value="Cancel" type="submit" />
</form>
