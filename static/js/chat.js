let chatSocket;
let typingTimer;
let isTyping = false;

function initChat(projectId, userId) {
    chatSocket = io("/chat");
    chatSocket.emit("join", { project_id: projectId });
  
    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");
    const messages = document.getElementById("chat-messages");
  
    // Handle form submission
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        if (input.value.trim()) {
            chatSocket.emit("send_message", {
                project_id: projectId,
                author_id: userId,
                text: input.value,
            });
            input.value = "";
            stopTyping();
        }
    });
  
    // Handle typing indicator
    input.addEventListener("input", () => {
        if (!isTyping) {
            isTyping = true;
            chatSocket.emit("typing", {
                project_id: projectId,
                user_id: userId,
                typing: true
            });
        }
        
        clearTimeout(typingTimer);
        typingTimer = setTimeout(stopTyping, 1000);
    });
    
    function stopTyping() {
        if (isTyping) {
            isTyping = false;
            chatSocket.emit("typing", {
                project_id: projectId,
                user_id: userId,
                typing: false
            });
        }
    }
  
    // Handle receiving messages
    chatSocket.on("receive_message", (data) => {
        const messageDiv = createMessageElement(data);
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
        
        // Play notification sound if not from current user
        if (data.author_id !== userId) {
            playNotificationSound();
        }
    });
    
    // Handle typing indicator
    chatSocket.on("user_typing", (data) => {
        updateTypingIndicator(data);
    });
}

function createMessageElement(data) {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const time = new Date(data.timestamp).toLocaleTimeString('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    div.innerHTML = `
        <div class="flex items-start space-x-2">
            <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                ${data.author_name ? data.author_name[0].toUpperCase() : 'U'}
            </div>
            <div class="flex-1">
                <div class="flex items-baseline space-x-2">
                    <span class="font-medium text-gray-800">${data.author_name || 'Utilisateur'}</span>
                    <span class="text-xs text-gray-500">${time}</span>
                </div>
                <p class="text-gray-700 mt-1">${escapeHtml(data.text)}</p>
            </div>
        </div>
    `;
    
    return div;
}

function updateTypingIndicator(data) {
    // Implementation for showing "User is typing..." indicator
    const typingDiv = document.getElementById('typing-indicator');
    if (typingDiv) {
        if (data.typing && data.user_id !== userId) {
            typingDiv.classList.remove('hidden');
        } else {
            typingDiv.classList.add('hidden');
        }
    }
}

function playNotificationSound() {
    // Create and play a subtle notification sound
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBiuBzvLZiTYIG2m98OScTgwOUarm7blmFgU7k9n1unEiBC13yO/eizEIHWq+8+OWT');
    audio.volume = 0.3;
    audio.play();
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}