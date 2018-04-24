% rebase('nonav_base.tpl', title="Cryptex Login")
<h1>Welcome to Cryptex</h1>
<p>Enter your master password to continue.</p>
<form action="/login" method="post">
    % if retry:
        <p class="error">Entered password didn't work. Please try again.</p>
    % end
    Password: <input name="password" type="password" autofocus />
    <input value="Log In" type="submit" />
</form>
