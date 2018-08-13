% rebase('nonav_base.tpl', title="New Entry")
% import shared_cfg
<h1>Create new entry</h1>
<form action="/manage-new-entry" method="post">
    % name = ""
    % username = ""
    % url = ""
    % if retry:
    %   name = data["name"]
    %   username = data["username"]
    %   url = data["url"]
    % end
    % if retry == "mismatch":
        <p class="error">Entered passwords did not match. Please try again.</p>
    % end
    % if retry == "duplicate":
        <p class="error">Entered entry name '{{name}}' is already used by an existing entry. Please try again.</p>
    % end
    % if retry == "bad_char":
        <p class="error">Entered entry name '{{name}}' contains one or more of the following characters, which are not allowed: {{shared_cfg.ILLEGAL_NAME_CHARS}}. Please try again.</p>
    % end
    % if retry == "no_name":
        <p class="error">Entries must have a name. Please try again.</p>
    % end
    % if retry == "other_error":
        <p class="error">An error occurred adding the entry. Please try again.</p>
    % end
    Name: <input name="name" type="text" value="{{name}}" autofocus/> <br>
    Username: <input name="username" type="text" value="{{username}}"/> <br>
    Password: <input name="password" type="password"/> <br>
    Re-enter Password: <input name="password2" type="password" /><br>
    URL: <input name="url" type="url" value="{{url}}"/> <br>
    <input name="create" value="Create" type="submit" />
    <input name="cancel" value="Cancel" type="submit" />
</form>
