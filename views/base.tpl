<!DOCTYPE html>
<html>
<head>
    <link href='/style.css' rel='stylesheet' type='text/css'/>
    <title>{{title or 'Cryptex'}}</title>
</head>
<body>
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