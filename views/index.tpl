% rebase('base.tpl', title=title)
<h1>Welcome to Cryptex</h1>
<p>Choose your destiny!</p>
<form action="/main_menu" method="post">
    <input type="submit" name="activate" value="Keyboard Mode">
    <input type="submit" name="manage" value="Manage Passwords">
    <input type="submit" name="master_pass" value="Change Master Password">
    <input type="submit" name="lock" value="Lock Everything">
</form>
