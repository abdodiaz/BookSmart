// === CONFIG ===
// Mets l'URL de ton backend FastAPI :
const API_BASE = "http://127.0.0.1:8000"; // ou http://localhost:8000

const form = document.getElementById("loginForm");
const alertBox = document.getElementById("alert");
const submitBtn = document.getElementById("submitBtn");
const spinner = document.getElementById("spinner");
const togglePwd = document.getElementById("togglePwd");
const pwdInput = document.getElementById("password");

// Afficher/Masquer mot de passe
togglePwd.addEventListener("click", () => {
  const isPwd = pwdInput.type === "password";
  pwdInput.type = isPwd ? "text" : "password";
});

// Utilitaire alert
function showAlert(message, type = "error") {
  alertBox.classList.remove("hidden");
  alertBox.textContent = message;
  if (type === "error") {
    alertBox.className = "mb-4 rounded-lg border border-red-200 bg-red-50 text-red-700 px-4 py-3 text-sm";
  } else {
    alertBox.className = "mb-4 rounded-lg border border-emerald-200 bg-emerald-50 text-emerald-700 px-4 py-3 text-sm";
  }
}

// State bouton
function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  spinner.classList.toggle("hidden", !isLoading);
}

// Submit handler (OAuth2PasswordRequestForm)
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  alertBox.classList.add("hidden");

  const email = form.email.value.trim();
  const password = form.password.value;

  if (!email || !password) {
    showAlert("Veuillez remplir tous les champs.");
    return;
  }

  try {
    setLoading(true);

    // OAuth2PasswordRequestForm attend du x-www-form-urlencoded:
    // fields: username, password, grant_type (optionnel)
    const body = new URLSearchParams();
    body.append("username", email);
    body.append("password", password);
    body.append("grant_type", "password");

    const res = await fetch(`${API_BASE}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      // IMPORTANT si ton backend met un cookie HttpOnly (set_cookie)
      credentials: "include"
    });

    const data = await res.json();

    if (!res.ok) {
      const detail = data?.detail || "Identifiants invalides.";
      showAlert(detail);
      return;
    }

    // Deux options côté backend :
    // 1) Tu renvoies access_token dans le JSON (et tu peux aussi mettre un cookie HttpOnly)
    // 2) Tu relies uniquement sur le cookie HttpOnly (credentials: 'include')
    if (data?.access_token) {
      localStorage.setItem("access_token", data.access_token);
    }

    showAlert("Connexion réussie. Redirection...", "success");
    // Redirection vers la Home (adapte le chemin selon tes routes)
    setTimeout(() => {
      window.location.href = "./home.html";
    }, 600);
  } catch (err) {
    showAlert("Erreur réseau. Vérifiez que l'API est démarrée.");
  } finally {
    setLoading(false);
  }
});
