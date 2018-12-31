% entryname = ''
% username = ''
% url = ''
% if data:
%   entryname = data['entryname']
%   username = data['username']
%   url = data['url']
% end
-->
<script src="js/jquery.min.js"></script>
<script src="js/cryptex.js"></script>
<script>
  setHTMLInputValue("entry-name-input", "{{entryname}}");
  setHTMLInputValue("user-name-input", "{{username}}");
  setHTMLInputValue("url-input", "{{url}}");
</script>
<!--
