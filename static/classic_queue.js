let searching = false;
let waitTime = 0;
let interval;


function startSearching() {
    if (searching) return;  // Évite le spam du bouton
        document.getElementById("searchButton").style.display = "none";
        searching = true;
        waitTime = 0;
        document.getElementById("waitingMessage").innerHTML = "Recherche de partie... 0s";

        interval = setInterval(async () => {
        waitTime+=1;
        document.getElementById("waitingMessage").innerHTML = `Recherche de partie... ${waitTime}s`;
        // Vérifie si une partie est disponible dans la base de données
        const response = await fetch("/check_game");
        const data = await response.json();
    
        if (data.ready) {setTimeout(()=> {window.location.href = "/game/"+data.gameid;}, 3000);}
        else{
            if(data.found){
                clearInterval(interval);
                document.getElementById("waitingMessage").innerHTML = "✅ Partie trouvée ! En attente de joueurs... veuillez patienter";
                //placer dans la queue
                await place_queue(data.gameid)
                let gameid = data.gameid
                //tant que la game n'est pas lancée, chaque seconde:
                setInterval(async () => {
                    const response = await fetch(`/wait_game?gameid=${gameid}`);
                    const data = await response.json();
                    if (data.ready) {setTimeout(()=> {window.location.href = "/game/"+gameid;}, 3000);}
                    console.log("OK OK OK")
                }, 5000)
                    
            }
        }
}, 1000);
}

async function place_queue(gameid){
    await fetch(`/ajouter_queue?gameid=${gameid}`);
}

async function launch_game(gameid){
    await fetch(`/launch_game?gameid=${gameid}`);
}