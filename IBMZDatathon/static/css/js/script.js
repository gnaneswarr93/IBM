async function sendMessage() {
    const input = document.getElementById("user-input").value;
    document.getElementById("chat-history").innerHTML += `<div class='message-box user-message'>${input}</div>`;
    document.getElementById("user-input").value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({message: input})
    });

    const data = await response.json();
    document.getElementById("chat-history").innerHTML += `<div class='message-box bot-message'>${data.reply}</div>`;
}
