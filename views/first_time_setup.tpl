% rebase('nonav_base.tpl', title="Cryptex Setup")
<h1>Setting up your Cryptex</h1>
<p>It looks like this is the first time this Cryptex has been used. Let's set it up!</p>
<form action="/first-time-setup" method="post">
    % if retry:
        <p class="error">Entered passwords did not match. Please try again.</p>
    % end
    Please enter the master password for the password database:</br>
    Password: <input name="password" type="password"/> </br>
    Re-enter Password: <input name="password2" type="password" /></br>
    <input value="Create" type="submit" />
</form>
