<?php

session_start();
// Inclure la connexion à la base de données
include 'includes/db_connection.php';

// Récupérer les utilisateurs de la base de données
$query = "SELECT * FROM users ORDER BY score DESC";
$users = $db->query($query)->fetchAll(PDO::FETCH_ASSOC);
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
            <?php
            //Si l'utilisateur n'est pas connecté, on propose un bouton connexion, deconnexion sinon.
            if(!$_SESSION){
                echo '<li><a href="connexion.php">Connexion</a></li>';
            }else{
                echo '<li><a href="disconnect.php">Deconnexion</a></li>';
            }
        
            ?>
        </ul>

    </nav>

    <main>
        <h2 class="leaderboard_title"> Leaderboard </h2>
        <?php foreach ($users as $user): ?>
            <li><?= htmlspecialchars($user['username']) ?> : <?= htmlspecialchars($user['score']) ?></li>
        <?php endforeach; ?>
    </main>

</body>



</html>