

    function createChatItem(message, sender) {
        var messages = document.getElementById("message_list");
        if (sender === "") {
          content = `<p>${message}</p>`;
        } else {
          var senderIsUser = "{{user}}" === sender;
          var content = `
          <li class="message">
              <p class="message">${sender} : ${message}</p>
          </li>
      `;}
        messages.innerHTML += content;
      }

      function sendMessage() {
        console.log("sendMessage() début de fonction")
        var msgInput = document.getElementById("monMessage");
        if (msgInput.value === "") return;
        var msg = msgInput.value;
        console.log(msg)
        socketio.emit("message", { message: msg });
        msgInput.value = "";
      }