% entry_name = ''
% username = ''
% url = ''
% if data:
%   if 'entry_name' in data.keys():
%       entry_name = data['entry_name']
%   end
%   if 'username' in data.keys():
%       username = data['username']
%   end
%   if 'url' in data.keys():
%       url = data['url']
%   end
% end
-->
<script src="js/jquery.min.js"></script>
<script src="js/cryptex.js"></script>
<script>
  setHTMLInputValue("entry-name-input", "{{entry_name}}");
  setHTMLInputValue("user-name-input", "{{username}}");
  setHTMLInputValue("url-input", "{{url}}");
</script>
<!--
