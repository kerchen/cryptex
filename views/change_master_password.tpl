% rebase('base.tpl', title="Change Master Password")
<h1>Changing Master Password</h1>
<form action="/change-master-password" method="post">
    % if bad_master:
        <p class="error">Entered master password was incorrect. Please try again.</p>
    % end
    % if mismatch:
        <p class="error">New passwords did not match. Please try again.</p>
    % end
    Existing Password: <input name="existing_password" type="password"/> </br>
    New Password: <input name="new_password" type="password"/> </br>
    Re-enter New Password: <input name="new_password_confirm" type="password" />
    <input value="Create" type="submit" />
</form>
