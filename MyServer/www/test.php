<?php $test = "bonbon";
session_start();
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <a href="./test2.php?valeur=<?=$test?>">GET TEST</a>
    <p>Post test</p>
    <form action="/koko.php" method="POST">
        <input type="text" name="nom" placeholder="Nom" id="nom">
        <input type="number" name="numero" id="">
        <input type="submit" value="Envoyer">
    </form>


</body>

</html>