% rebase('nonav_base.tpl', title="Edit Entry")
% import shared_cfg
% folders = path.split("/")
<h1>Editing {{path}}</h1>
<br>
% name, entry = shared_cfg.get_entry_by_path(path)
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
<p class="error">Entered entry name '{{name}}' is already used by another entry. Please try again.</p>
% end
% if retry == "bad_char":
<p class="error">Entered entry name '{{name}}' contains one or more disallowed characters. Please limit names to these characters: {{shared_cfg.LEGAL_NAME_CHARS}}. Please try again.</p>
% end
% if retry == "no_name":
<p class="error">Entries must have a name. Please try again.</p>
% end
% if retry == "other_error":
<p class="error">An error occurred updating the entry. Please try again.</p>
% end
Name: <input id="name" type="text" value="{{name}}" autofocus/> <br>
Username: <input id="username" type="text" value="{{entry.get_username()}}"/> <br>
Password: <input id="password" type="password" value="{{entry.get_password()}}"/> <br>
Re-enter Password: <input id="password2" type="password" value="{{entry.get_password()}}"/> <br>
URL: <input id="url" type="url" value="{{entry.get_url()}}"/> <br>
<br>
<button onclick="update_entry()">Update Entry</button>
<button onclick="confirm_remove()">Remove Entry</button>
<button onclick="cancel()">Cancel</button>
<script>
    function update_entry() {
        post('/updateentry'+'{{path}}',
             {name: document.getElementById("name").value,
              username: document.getElementById("username").value,
              password: document.getElementById("password").value,
              password2: document.getElementById("password2").value,
              url: document.getElementById("url").value}, "post");
    }

    function confirm_remove() {
        var response = confirm("Remove the entry '{{path}}'?");
        if (response == true) {
            post('/removeentry'+'{{path}}', {}, "post");
        }
    }

    function cancel() {
        var response = confirm("Cancel editing this entry?");
        if (response == true) {
            post('/cancelupdate'+'{{path}}', {}, "post");
        }
    }
</script>
<br>
