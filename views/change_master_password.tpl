% rebase('nonav_base.tpl', title="Change Master Password")
<h1>Changing Master Password</h1>
<form action="/change-master-password" method="post">
    % if bad_master:
        <p class="error">Entered master password was incorrect. Please try again.</p>
    % end
    % if mismatch:
        <p class="error">New passwords did not match. Please try again.</p>
    % end
    <table>
        <tr>
            <th>Existing Password:</th>
            <th><input name="existing_password" type="password" autofocus/></th>
        </tr>
        <tr>
            <th>New Password:</th>
            <th><input name="new_password" type="password"/></th>
        </tr>
        <tr>
            <th>Re-enter New Password:</th>
            <th><input name="new_password_confirm" type="password" /></th>
        </tr>
    </table>
    <input value="Change" name="change" type="submit" /> <input value="Cancel" name="cancel" type="submit" />
</form>
