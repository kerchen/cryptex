% include('password_generator.tpl')
% entry_name = ''
% username = ''
% url = ''
% password1 = ''
% password2 = ''
% if data:
    % if 'entry_name' in data.keys():
        % entry_name = data['entry_name']
    % end
    % if 'username' in data.keys():
        % username = data['username']
    % end
    % if 'url' in data.keys():
        % url = data['url']
    % end
    % if 'password1' in data.keys():
        % password1 = data['password1']
    % end
    % if 'password2' in data.keys():
        % password2 = data['password2']
    % end
% end
-->
<script src="js/jquery.min.js"></script>
<script src="js/cryptex.js"></script>
<script>
  setHTMLInputValue("entry-name-input", "{{entry_name}}");
  setHTMLInputValue("user-name-input", "{{username}}");
  setHTMLInputValue("password-input", "{{password1}}");
  setHTMLInputValue("password-confirm-input", "{{password2}}");
  setHTMLInputValue("url-input", "{{url}}");

  function onPasswordAccepted(encodedPassword) {
    var decodedPassword = decodeHTML(encodedPassword);
    console.log("Got password: " + decodedPassword);
    setHTMLInputValue("password-input", decodedPassword);
    setHTMLInputValue("password-confirm-input", decodedPassword);
  }

  function copyPasswordToClipboard() {
    var pwInput = document.getElementById('password-input');

    // TODO: Verify that this works with all browsers!
    var textArea = document.createElement('textarea');
    textArea.setAttribute('style','width:1px;border:0;opacity:0;');
    document.body.appendChild(textArea);
    textArea.value = pwInput.value;
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
  }
</script>
<!--
