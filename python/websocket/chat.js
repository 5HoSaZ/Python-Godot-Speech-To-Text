const ws = new WebSocket("ws://localhost:8765");
let username;

ws.onopen = () => {
  console.log("Connected to the WebSocket server");
  username = prompt("Enter your username:");
  ws.send(username); // Get user name
};

ws.onmessage = (event) => {
  const chatbox = document.getElementById("chatbox");
  const message = document.createElement("div");
  message.textContent = event.data;
  chatbox.appendChild(message);
};

function sendMessage() {
  const input = document.getElementById("message");
  const message = `${username}: ${input.value}`;
  ws.send(message);
  input.value = "";
}
