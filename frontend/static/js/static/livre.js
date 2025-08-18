const bookImage = document.getElementById("bookImage");
const bookTitle = document.getElementById("bookTitle");
const bookPrice = document.getElementById("bookPrice");
const bookDescription = document.getElementById("bookDescription");
const bookStatus = document.getElementById("bookStatus");
const reserveButton = document.getElementById("reserveButton");
const messageElement = document.getElementById("message");

// Récupérer l'id du livre depuis l'URL : livre.html?id=123
const urlParams = new URLSearchParams(window.location.search);
const bookId = urlParams.get("id");

// Fonction pour charger les infos du livre
async function fetchBook() {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/livres/${bookId}`);
    const book = await response.json();

    bookImage.src = book.image_url;
    bookTitle.textContent = book.titre;
    bookPrice.textContent = `${book.prix} €`;
    bookDescription.textContent = book.description || "Pas de description disponible.";

    if (book.stock > 0) {
      bookStatus.textContent = "Disponible";
      bookStatus.className = "px-2 py-1 text-sm font-semibold rounded-full bg-green-200 text-green-800";
      reserveButton.disabled = false;
    } else {
      bookStatus.textContent = "Réservé";
      bookStatus.className = "px-2 py-1 text-sm font-semibold rounded-full bg-red-200 text-red-800";
      reserveButton.disabled = true;
    }

  } catch (error) {
    messageElement.textContent = "Erreur lors du chargement du livre.";
    reserveButton.disabled = true;
  }
}

// Fonction pour réserver le livre
reserveButton.addEventListener("click", async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/reservations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_livre: bookId })  // id_adherent récupéré côté backend via JWT
    });

    const data = await response.json();
    if (response.ok) {
      messageElement.classList.remove("text-red-500");
      messageElement.classList.add("text-green-500");
      messageElement.textContent = "Réservation réussie !";
      reserveButton.disabled = true;
      bookStatus.textContent = "Réservé";
      bookStatus.className = "px-2 py-1 text-sm font-semibold rounded-full bg-red-200 text-red-800";
    } else {
      messageElement.textContent = data.detail || "Impossible de réserver ce livre.";
    }
  } catch (error) {
    messageElement.textContent = "Erreur lors de la réservation.";
  }
});

// Chargement initial
fetchBook();
