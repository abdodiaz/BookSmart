document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();
  
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirmPassword").value.trim();
    const messageElement = document.getElementById("message");
  
    if (password !== confirmPassword) {
      messageElement.textContent = "Les mots de passe ne correspondent pas.";
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
      });
  
      const data = await response.json();
  
      if (response.ok) {
        messageElement.classList.remove("text-red-500");
        messageElement.classList.add("text-green-500");
        messageElement.textContent = "Inscription réussie ! Redirection...";
        setTimeout(() => { window.location.href = "login.html"; }, 1500);
      } else {
        messageElement.classList.remove("text-green-500");
        messageElement.classList.add("text-red-500");
        messageElement.textContent = data.detail || "Erreur lors de l'inscription.";
      }
    } catch (error) {
      messageElement.textContent = "Erreur de connexion au serveur.";
    }
  });
  