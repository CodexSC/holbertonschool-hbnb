import { apiRequest } from "./api.js";
import { bindLogout, getTokenCookie } from "./auth.js";

const placesList = document.getElementById("places-list");
const priceFilter = document.getElementById("price-filter");
const message = document.getElementById("message");
const loginLink = document.getElementById("login-link");
const logoutLink = document.getElementById("logout-link");
const PRICE_FILTER_OPTIONS = [10, 50, 100];

let allPlaces = [];

initializePage();

function initializePage() {
  if (!placesList || !priceFilter || !message) {
    console.error("Required index page elements are missing.");
    return;
  }

  configureAuthNavigation();
  initializePriceFilter();
  bindLogout("#logout-link");
  priceFilter.addEventListener("change", onPriceChange);
  loadPlaces();
}

function configureAuthNavigation() {
  const token = getTokenCookie();
  const isAuthenticated = Boolean(token);

  if (loginLink) {
    loginLink.style.display = isAuthenticated ? "none" : "inline-flex";
  }

  if (logoutLink) {
    logoutLink.style.display = isAuthenticated ? "inline-flex" : "none";
  }
}

function initializePriceFilter() {
  priceFilter.innerHTML = "";

  const allOption = document.createElement("option");
  allOption.value = "all";
  allOption.textContent = "All";
  priceFilter.appendChild(allOption);

  for (const price of PRICE_FILTER_OPTIONS) {
    const option = document.createElement("option");
    option.value = String(price);
    option.textContent = String(price);
    priceFilter.appendChild(option);
  }
}

async function loadPlaces() {
  try {
    const token = getTokenCookie();
    const payload = await apiRequest("/places", {}, token);
    const places = Array.isArray(payload)
      ? payload
      : payload?.results || payload?.data || [];

    allPlaces = places.map(normalizePlace);
    renderPlaces(places);
    applyPriceFilter(priceFilter.value);
  } catch (error) {
    showMessage(error.message || "Could not fetch places.", true);
  }
}

function normalizePlace(place) {
  const priceValue = Number(place.price_by_night ?? place.price ?? NaN);
  const resolvedPrice = Number.isFinite(priceValue) ? priceValue : null;

  return {
    ...place,
    _resolvedPrice: resolvedPrice,
    _location: resolveLocation(place)
  };
}

function renderPlaces(places) {
  placesList.textContent = "";

  if (!places.length) {
    showMessage("No places available right now.", false);
    return;
  }

  showMessage("", false);

  const cardsFragment = document.createDocumentFragment();

  for (const place of allPlaces) {
    cardsFragment.appendChild(createPlaceCard(place));
  }

  placesList.appendChild(cardsFragment);
}

function createPlaceCard(place) {
  const card = document.createElement("article");
  card.className = "place-card";
  card.dataset.price = String(place._resolvedPrice ?? "");

  const name = document.createElement("h3");
  name.textContent = place.name || "Unnamed place";

  const description = document.createElement("p");
  description.className = "place-meta";
  description.textContent =
    place.description || "No description available for this place.";

  const location = document.createElement("p");
  location.className = "place-meta";
  location.textContent = `Location: ${place._location || "Not specified"}`;

  const price = document.createElement("p");
  price.className = "price";
  price.textContent = `Price per night: ${formatPrice(place)}`;

  const detailsButton = document.createElement("a");
  detailsButton.className = "details-button";
  detailsButton.href = `place.html?id=${encodeURIComponent(place.id || "")}`;
  detailsButton.textContent = "View Details";

  card.append(name, description, location, price, detailsButton);
  return card;
}

function formatPrice(place) {
  return place._resolvedPrice !== null ? `$${place._resolvedPrice}` : "N/A";
}

function resolveLocation(place) {
  return (
    place.location ||
    place.city?.name ||
    place.city ||
    place.country?.name ||
    place.country ||
    ""
  );
}

function onPriceChange(event) {
  applyPriceFilter(event.target.value);
}

function applyPriceFilter(selectedValue) {
  const cardElements = placesList.querySelectorAll(".place-card");
  const maxPrice = selectedValue === "all" ? null : Number(selectedValue);
  let visibleCount = 0;

  for (const card of cardElements) {
    const placePrice = Number(card.dataset.price);
    const isVisible =
      maxPrice === null || (Number.isFinite(placePrice) && placePrice <= maxPrice);

    card.style.display = isVisible ? "" : "none";
    if (isVisible) {
      visibleCount += 1;
    }
  }

  if (visibleCount === 0) {
    showMessage("No places match the selected maximum price.", false);
  } else {
    showMessage("", false);
  }
}

function showMessage(text, isError) {
  message.textContent = text;
  message.className = "message";
  if (text) {
    message.classList.add(isError ? "error" : "success");
  }
}
