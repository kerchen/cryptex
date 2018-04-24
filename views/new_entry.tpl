% rebase('nonav_base.tpl', title="New Entry")
<h1>Create new entry</h1>
<form action="/manage-new-entry" method="post">
    % if retry:
    <p class="error">Entered passwords did not match. Please try again.</p>
    % end
    Name: <input name="name" type="text"/> </br>
    Username: <input name="username" type="text"/> </br>
    Password: <input name="password" type="password"/> </br>
    Re-enter Password: <input name="password2" type="password" /></br>
    URL: <input name="url" type="url"/> </br>
    <input name="create" value="Create" type="submit" />
    <input name="cancel" value="Cancel" type="submit" />
</form>
