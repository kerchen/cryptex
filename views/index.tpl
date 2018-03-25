% rebase('base.tpl', title="Cryptex")
<h1>Welcome to Cryptex</h1>
<form action="/main_menu" method="post">
    % if status_msg:
    <p class="result">{{status_msg}}</p>
    % else:
    <p>Choose your destiny!</p>
    % end
    <input type="submit" name="activate" value="Keyboard Mode">
    <input type="submit" name="manage" value="Manage Passwords">
    <input type="submit" name="master_pass" value="Change Master Password">
    <input type="submit" name="lock" value="Lock Everything">
</form>
