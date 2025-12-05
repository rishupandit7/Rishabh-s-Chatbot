const messages = document.getElementById("messages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const toggleBtn = document.getElementById("toggleMode");

let BOT_NAME = "Rishu AI ChatB🤖t";

window.onload = () => {
    messages.innerHTML = "";
};  


function saveChat() {
    localStorage.setItem("chat", messages.innerHTML);
}

toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
});

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage("user", text);
    userInput.value = "";

    typingAnimation(true);

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    })
        .then(res => res.json())
        .then(data => {
            typingAnimation(false);
            if (data.bot_name) BOT_NAME = data.bot_name;
            addMessage("bot", data.reply);
        })
        .catch(() => {
            typingAnimation(false);
            addMessage("bot", "Something went wrong. Please Try again.");
        });
}

function typingAnimation(show) {
    if (show) {
        const div = document.createElement("div");
        div.className = "message bot typing";
        div.id = "typingMessage";
        div.innerHTML = `<div class="icon"></div> ${BOT_NAME} is typing...`;
        messages.appendChild(div);
        scrollDown();
    } else {
        const t = document.getElementById("typingMessage");
        if (t) t.remove();
    }
}

function addMessage(type, text) {
    const div = document.createElement("div");
    div.className = `message ${type}`;
    div.innerHTML = `
        <div class="icon"></div>
        ${text}
    `;
    messages.appendChild(div);
    scrollDown();
}

function scrollDown() {
    messages.scrollTop = messages.scrollHeight;
}
