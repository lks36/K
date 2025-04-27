

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

var input = document.getElementById("monMessage");

input.addEventListener("keypress", function(event) {
  console.log('enter');
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("send_button").click();
  }
}); 