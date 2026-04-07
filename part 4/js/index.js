import { apiRequest } from "./api.js";
import { bindLogout, getTokenCookie, requireAuth } from "./auth.js";

const placesList = document.getElementById("places-list");
const countryFilter = document.getElementById("country-filter");
const message = document.getElementById("message");

let allPlaces = [];

if (!requireAuth("login.html")) {
  throw new Error("User is not authenticated.");
}

bindLogout("#logout-link");
loadPlaces();

countryFilter?.addEventListener("change", () => {
  renderPlaces(filterPlacesByCountry(countryFilter.value));
});

async function loadPlaces() {
  try {
    const token = getTokenCookie();
    const payload = await apiRequest("/places", {}, token);
    const places = Array.isArray(payload) ? payload : payload?.results || payload?.data || [];

    allPlaces = places;
    populateCountryFilter(places);
    renderPlaces(places);
  } catch (error) {
    showMessage(error.message || "Could not fetch places.", true);
  }
}

function populateCountryFilter(places) {
  const countries = [...new Set(places.map((place) => getCountryName(place)).filter(Boolean))].sort();

  for (const country of countries) {
    const option = document.createElement("option");
    option.value = country;
    option.textContent = country;
    countryFilter.appendChild(option);
  }
}

function filterPlacesByCountry(country) {
  if (!country) {
    return allPlaces;
  }

  return allPlaces.filter((place) => getCountryName(place) === country);
}

function getCountryName(place) {
  return (
    place.country?.name ||
    place.country ||
    place.location?.country ||
    place.city?.country?.name ||
    ""
  );
}

function renderPlaces(places) {
  placesList.textContent = "";

  if (!places.length) {
    showMessage("No places found for the selected country.", false);
    return;
  }

  showMessage("", false);

  for (const place of places) {
    const card = document.createElement("article");
    card.className = "place-card";

    const name = document.createElement("h3");
    name.textContent = place.name || "Unnamed place";

    const price = document.createElement("p");
    price.className = "price";
    const value = Number(place.price_by_night ?? place.price ?? 0);
    price.textContent = `Price per night: $${Number.isNaN(value) ? "N/A" : value}`;

    const detailsButton = document.createElement("a");
    detailsButton.className = "details-button";
    detailsButton.href = `place.html?id=${encodeURIComponent(place.id)}`;
    detailsButton.textContent = "View Details";

    card.append(name, price, detailsButton);
    placesList.appendChild(card);
  }
}

function showMessage(text, isError) {
  message.textContent = text;
  message.className = "message";
  if (text) {
    message.classList.add(isError ? "error" : "success");
  }
}
