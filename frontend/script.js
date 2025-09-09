// Al cargar la página, limpiamos el chat y el input
window.onload = () => {
  document.getElementById("chat-box").innerHTML = "";
  document.getElementById("user-input").value = "";
};

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  // Mostrar mensaje del usuario
  addMessage(message, "user");
  input.value = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error("Error en la respuesta del servidor");
    }

    const data = await response.json();

    // ✅ Siempre mostrar solo la respuesta del bot (string)
    addMessage(data.response, "bot");

    // 🔍 Opcional: ver debug por consola sin romper el chat
    if (data.debug) {
      console.log("🔍 Debug NLP:", data.debug);
    }

  } catch (error) {
    addMessage("❌ Hubo un problema al conectar con el servidor.", "bot");
    console.error("Error en sendMessage:", error);
  }
}

function addMessage(text, sender) {
  const chatBox = document.getElementById("chat-box");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message " + sender;
  messageDiv.innerHTML = text; // 👈 aquí renderiza etiquetas HTML
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Enviar con botón
document.getElementById("send-btn").addEventListener("click", sendMessage);

// Enviar con Enter
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault(); 
    sendMessage();
  }
});
