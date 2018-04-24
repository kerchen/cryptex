% rebase('base.tpl', title="Cryptex")
<h1>Welcome to Cryptex</h1>
<form action="/main_menu" method="post">
    % if status_msg:
    <p class="result">{{status_msg}}</p>
    % else:
    <p>Choose your destiny!</p>
    % end
</form>
