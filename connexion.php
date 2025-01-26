<?php
// Connectez-vous à la base de données SQLite
try {
    $db = new PDO('sqlite:./database/database.db'); // Assurez-vous que le chemin est correct
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erreur de connexion à la base de données : " . $e->getMessage());
}


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email']);
    $password = trim($_POST['password']);

    
    $stmt = $db->prepare("SELECT * FROM users WHERE email = :email");
    $stmt->bindParam(':email', $email);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && $password === $user['password']) {
        sleep(1);
        // Redirigez ou lancez une session ici
        session_start();
        $_SESSION['user'] = $user;
        header('Location: index.php');
        exit;
    } else {
        echo '<script>alert("Utilisateur introuvable ou mot de passe incorrect.")</script>';
    }
}
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


    <main class="login_box">
        <div class="login">
            

            <div class="connexion">
            <p class="title">Connexion à K</p>
                <form method="post" class="login_form">
                    <div class="login_form">
                        <input type="email" id="email" name="email" class="input" autocomplete="off" placeholder="Entrez votre email" required>
                    </div>
                    <div>
                        <input type="password" id="password" name="password" class="input" autocomplete="off" placeholder="Entrez votre mot de passe" required>
                    </div>
                        <span class="page-link-label">Mot de passe oublié ?</span>
                    <div>
                    
                    </div>
                    <p></p>
                        <button type="submit" class="form-btn">Se connecter</button>
                    <div><p class="sign-up-label">Pas de compte ? <span class="sign-up-link">S'inscrire</span></p></div>
                    
                </form>
            </div>
        </div>
        
    </main>

</body>