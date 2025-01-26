<?php
try {
    // Chemin vers votre fichier SQLite
    $db = new PDO('sqlite:' . __DIR__ . '/../database/database.db');

    // Configurer PDO pour lever des exceptions en cas d'erreur
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo "Erreur de connexion : " . $e->getMessage();
    exit;
}
?>
