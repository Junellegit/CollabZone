function initChat(projectId, userId) {
    const chatSocket = io("/chat");
    chatSocket.emit("join", { project_id: projectId });
  
    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");
    const messages = document.getElementById("messages");
  
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (input.value.trim()) {
        chatSocket.emit("send_message", {
          project_id: projectId,
          author_id: userId,
          text: input.value,
        });
        input.value = "";
      }
    });
  
    chatSocket.on("receive_message", (data) => {
      const div = document.createElement("div");
      div.textContent = data.text;
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    });
  }