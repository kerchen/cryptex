% rebase('nonav_base.tpl', title="New Folder")
% import shared_cfg
<h1>Create new folder</h1>
<form action="/manage-new-container" method="post">
    % name = ""
    % if retry:
    %   name = data["name"]
    % end
    % if retry == "no_name":
        <p class="error">Folder names cannot be empty. Please try again.</p>
    % end
    % if retry == "duplicate":
        <p class="error">Entered folder name '{{name}}' already exists. Please try again.</p>
    % end
    % if retry == "bad_char":
        <p class="error">Entered folder name '{{name}}' contains one or more of the following disallowed characters: {{shared_cfg.ILLEGAL_NAME_CHARS}}. Please try again.</p>
    % end
    % if retry == "other_error":
        <p class="error">An error occurred adding the folder. Please try again.</p>
    % end
    Name: <input name="name" type="text" value="{{name}}" autofocus/> </br>
    <input name="create" value="Create" type="submit" />
    <input name="cancel" value="Cancel" type="submit" />
</form>
