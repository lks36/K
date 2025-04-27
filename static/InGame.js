var sessionid;
var socketio = io();
var status;
var talking;
var talking_text = document.getElementById("talking");
var team1;
var team2;
var room = sessionStorage;
var response = null;
var nb_likes = 6;
var barre_texte = document.getElementById("monMessage");
let muted = "<p>Vous ne pouvez pas parler car ce n'est pas votre tour.</p>"
var div_bottom = document.getElementById("bottom");
let default_bottom = div_bottom.innerHTML;
let response_bottom = `<button onclick=annuler()>annuler</button>`+ default_bottom;
let send_button = document.getElementById("send_button");
var input = document.getElementById("monMessage");
var message_box = document.getElementById("message_ul");
div_bottom.innerHTML = muted;

function createChatItem(id, message, sender, date, equipe, avatar, rep) {
    if(rep){response=rep;}
    if(response === 0){console.log(id+"veut répondre à"+response);}
    if(equipe === null){return;}
    var messages = document.getElementById("message_ul");
    if (sender === "") {
      content = `<p>${message}</p>`;
    } else {
      var senderIsUser = "{{user}}" === sender;
      var content = `

      <div class="message_container${equipe}" id=${id}>
      <img class="avatar" src="/static/avatars/${avatar}.jpg">
          
          <div class="message_content">
            <p class="pseudo">${sender}</p>
            <p class="message">${message}</p>
            
          </div>
          
          </div>
          <div class="buttons">
          <button class="reply" onclick="setresponse(${id})">repondre</button>
          `
          if(nb_likes > 0){content+= `<button class="like" onclick="like_message(${id})">j'aime (${nb_likes})</button>`}
          
          `
          `
          if(response != null){content+= `<a class="origin" href="#${response}" onclick=surligner(${response})> voir le message ciblé </a>`}
          content += 
          `
          </div>
          `
          ;}
    messages.innerHTML += content;
    response = null;
    if(input){
      annuler();
    }
  }

function sendMessage() {
  var msgInput = document.getElementById("monMessage");
  if (msgInput.value === "") return;
  var msg = msgInput.value;
  socketio.emit("message", { message: msg , rep: response});
  msgInput.value = "";
  demanderInfos();
}




function like_message(id){

  let likes = document.getElementsByClassName("like");
  if(nb_likes === 0){return;}
  
  nb_likes = nb_likes - 1;
  if(nb_likes === 0){delete_likes(likes);}
  for(let i=0; i<likes.length; i++){
    likes[i].innerHTML = `j'aime (${nb_likes})`;
  }
  
  //Envoyer le like avec le socket et le gérer côté python
  socketio.emit("like", {message_id:id});

}


function delete_likes(array){
  if(array.length === 0) return;
  array[0].remove();
  delete_likes(array);
}



function restore_listener(){
  input = document.getElementById("monMessage");
  input.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      // Trigger the button element with a click
      send_button.click();
    }
  }); 
}


function setresponse(id){
  if(div_bottom.innerHTML != muted){
  response = id;
  div_bottom.innerHTML = response_bottom;
  restore_listener();
  barre_texte = document.getElementById("monMessage");
  barre_texte.placeholder="Répondre";
  }
}

function annuler(){
  if(div_bottom.innerHTML != muted){
  div_bottom.innerHTML = default_bottom;
  response = null;
  restore_listener();}
}


function surligner(response){

  var message = document.getElementById(response);
  var old = message.style.backgroundColor;
  
  message.style.backgroundColor = "rgb(179, 181, 214)"
  setTimeout(()=>{message.style.backgroundColor = old;}, 1000);
  

}

function demanderInfos(){
  socketio.emit("update", null);
}

function updateInfos(id, gameStatus, gameTalking, ListeEquipe1, ListeEquipe2, time, round){
    status = gameStatus;
    talking = gameTalking;
    if(gameTalking){
      talking_text.innerHTML = "Au tour de " + gameTalking;
    }
    else{
      talking_text.innerHTML = "Veuillez patienter"
    }
    var timer = document.getElementById("timer");
    timer.innerHTML = `<h3 id="timer">Temps restant : ${time}s</h3>`

    /*Mettre a jour le round*/
    var tour = document.getElementById("tour");
    tour.innerHTML = `<h3 id="round">Round : ${round}/3</h3>`
    /* Mettre a jour les équipes */
    var equipe1 = document.getElementById("equipe1");
    var equipe2 = document.getElementById("equipe2");


    var c1 = "";
    for(const username of ListeEquipe1){
      c1 += "<p>"+username+"</p>";
    }
    equipe1.innerHTML = c1;

    var c2 = "";
    for(const username of ListeEquipe2){
      c2 += "<p>"+username+"</p>";
    }
    equipe2.innerHTML = c2;



    /* Verifier si c'est au tour du joueur de parler */
    if(id===sessionid || round === 0){
      /* Activer la barre de texte et activer le bouton entrer pour envoyer */
      if(div_bottom.innerHTML === muted){
        div_bottom.innerHTML = default_bottom;
        restore_listener();
      }
      
    }
    else{
      /* Desactiver la barre de texte */
      div_bottom.innerHTML = muted;
    }

}

demanderInfos();
setInterval(async () => {
  await console.log("test");
  await demanderInfos();
}, 1000)