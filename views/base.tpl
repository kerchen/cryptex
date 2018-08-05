<!DOCTYPE html>
<html>
<head>
    <link href='/style.css' rel='stylesheet' type='text/css'/>
    <title>{{title or 'Cryptex'}}</title>
</head>
<body>
<script>
    function post(path, params, method) {
        method = method || "post"; // Set method to post by default if not specified.

        // The rest of this code assumes you are not using a library.
        // It can be made less wordy if you use one.
        var form = document.createElement("form");
        form.setAttribute("method", method);
        form.setAttribute("action", path);

        for(var key in params) {
            if(params.hasOwnProperty(key)) {
                var hiddenField = document.createElement("input");
                hiddenField.setAttribute("type", "hidden");
                hiddenField.setAttribute("name", key);
                hiddenField.setAttribute("value", params[key]);

                form.appendChild(hiddenField);
            }
        }

        document.body.appendChild(form);
        form.submit();
    }
</script>
    {{!base}}

    <footer>
        <form action="/footer" method="post">
            <input type="submit" name="activate" value="Keyboard Mode">
            <input type="submit" name="manage" value="Manage Passwords">
            <input type="submit" name="master_pass" value="Change Master Password">
            <input type="submit" name="lock" value="Lock Everything">
        </form>
    </footer>
</body>
</html>