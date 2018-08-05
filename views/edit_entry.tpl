% rebase('base.tpl', title=title)
% import shared_cfg
% folders = path.split("/")
<p><b>Editing {{path}}</b></p>
% e_name, e = shared_cfg.get_entry_by_path(path)
% print(e.get_username())
% print(e.get_password())
</br>
Name: <input name="name" type="text" value="{{e_name}}" autofocus/> </br>
Username: <input name="username" type="text" value="{{e.get_username()}}"/> </br>
Password: <input name="password" type="password" value="{{e.get_password()}}"/> </br>
URL: <input name="url" type="url" value="{{e.get_url()}}"/> </br>
</br>
<button onclick="update_entry()">Update Entry</button>
<button onclick="confirm_remove()">Remove Entry</button>
<script>
    function confirm_remove() {
        var response = confirm("Remove the entry '{{path}}'?");
        if (response == true) {
            post('/removeentry'+'{{path}}', {}, "post");
        }
    }
</script>
<br/>
