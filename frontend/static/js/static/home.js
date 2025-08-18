const booksContainer = document.getElementById("booksContainer");
const searchInput = document.getElementById("searchInput");

// Fonction pour récupérer les livres depuis l'API
async function fetchBooks(query = "") {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/livres?search=${query}`);
    const books = await response.json();
    displayBooks(books);
  } catch (error) {
    booksContainer.innerHTML = "<p class='text-red-500'>Erreur lors du chargement des livres.</p>";
  }
}

// Fonction pour afficher les livres dans la grille
function displayBooks(books) {
  if (books.length === 0) {
    booksContainer.innerHTML = "<p class='text-gray-500 col-span-full'>Aucun livre trouvé.</p>";
    return;
  }

  booksContainer.innerHTML = books.map(book => `
    <div class="bg-white rounded-lg shadow p-4 flex flex-col">
      <img src="${book.image_url}" alt="${book.titre}" class="h-48 w-full object-cover rounded-md mb-4">
      <h2 class="font-semibold text-lg text-gray-800 mb-2">${book.titre}</h2>
      <p class="text-sm mb-2">${book.prix} €</p>
      <span class="px-2 py-1 text-sm font-semibold rounded-full ${book.stock > 0 ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}">
        ${book.stock > 0 ? 'Disponible' : 'Réservé'}
      </span>
    </div>
  `).join('');
}

// Rechercher en tapant
searchInput.addEventListener("input", () => {
  fetchBooks(searchInput.value.trim());
});

// Chargement initial
fetchBooks();
