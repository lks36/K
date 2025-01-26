<?php

session_start();

// Inclure la connexion à la base de données
include 'includes/db_connection.php';

// Récupérer les utilisateurs de la base de données
$query = "SELECT * FROM users";
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
        <div>
            <ul>
                <li><a href="">Acceuil</a></li>
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
        </div>
        <div class="profile">
            <ul>
                <?php if($_SESSION){echo '<li class="profile_button"><a href="profile.php">'. $_SESSION['user']['username'] .'</a></li>';}?>
            </ul>
        </div>

    </nav>

    <main>
        <?php
        //Si l'utilisateur est connecté, on affiche un message de bienvenue
        if($_SESSION){
            echo "<h3> Bienvenue dans K " . $_SESSION['user']['username'] . "</h3>";
        }
        ?>
        
        
    </main>

</body>



</html>