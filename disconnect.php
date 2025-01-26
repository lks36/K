<?php
    sleep(1);
    session_start();
    session_destroy();
?>



<!DOCTYPE html>
<html>
<head>
    <title>Accueil</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="styles.css">
</head>

<body>
    <nav class="navbar">
        <ul>
            <li><a href="index.php">Acceuil</a></li>
            <li><a href="">Comment jouer ?</a></li>
            <li><a href="leaderboard.php">Leaderboard</a></li>
        </ul>

    </nav>

    <main>
        <h1>Vous avez été déconnecté !</h1>
    </main>

</body>



</html>