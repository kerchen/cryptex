% entryname = ''
% username = ''
% url = ''
% password1 = ''
% password2 = ''
% if data:
%   entryname = data['entryname']
%   username = data['username']
%   url = data['url']
%   password1 = data['password1']
%   password2 = data['password2']
% end
-->
<script src="js/jquery.min.js"></script>
<script src="js/cryptex.js"></script>
<script>
  setHTMLInputValue("entry-name-input", "{{entryname}}");
  setHTMLInputValue("user-name-input", "{{username}}");
  setHTMLInputValue("password-input", "{{password1}}");
  setHTMLInputValue("password-confirm-input", "{{password2}}");
  setHTMLInputValue("url-input", "{{url}}");
</script>
<!--
