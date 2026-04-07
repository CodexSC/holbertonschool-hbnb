import { apiRequest } from "./api.js";
import { getTokenCookie, isAuthenticated } from "./auth.js";

const placeDetails = document.getElementById("place-details");
const reviewsList = document.getElementById("reviews-list");
const message = document.getElementById("message");
const addReviewSection = document.getElementById("add-review-access");
const addReviewButton = document.getElementById("add-review-button");

const params = new URLSearchParams(window.location.search);
const placeId = params.get("id");

if (!placeId) {
  setError("Place id missing from URL.");
} else {
  initializePage();
}

async function initializePage() {
  try {
    const token = getTokenCookie();
    const place = await apiRequest(`/places/${encodeURIComponent(placeId)}`, {}, token || null);
    renderPlace(place);

    const reviews = await fetchPlaceReviews(placeId, token || null);
    renderReviews(reviews);

    if (isAuthenticated()) {
      addReviewSection.classList.remove("hidden");
      addReviewButton.href = `add_review.html?place_id=${encodeURIComponent(placeId)}`;
    }
  } catch (error) {
    setError(error.message || "Could not load place details.");
  }
}

async function fetchPlaceReviews(id, token) {
  try {
    const payload = await apiRequest(`/places/${encodeURIComponent(id)}/reviews`, {}, token);
    return Array.isArray(payload) ? payload : payload?.results || payload?.data || [];
  } catch (error) {
    const fallback = await apiRequest(`/reviews?place_id=${encodeURIComponent(id)}`, {}, token);
    return Array.isArray(fallback) ? fallback : fallback?.results || fallback?.data || [];
  }
}

function renderPlace(place) {
  const amenities = Array.isArray(place.amenities)
    ? place.amenities.map((item) => item.name || item).join(", ")
    : "No amenities listed";

  const hostName =
    place.host?.first_name && place.host?.last_name
      ? `${place.host.first_name} ${place.host.last_name}`
      : place.host?.name || "Unknown host";

  const lines = [
    `<h2>${escapeHtml(place.name || "Place")}</h2>`,
    `<p class="place-meta">Host: ${escapeHtml(hostName)}</p>`,
    `<p class="place-meta">Price per night: $${escapeHtml(String(place.price_by_night ?? place.price ?? "N/A"))}</p>`,
    `<p class="place-meta">Description: ${escapeHtml(place.description || "No description provided")}</p>`,
    `<p class="place-meta">Amenities: ${escapeHtml(amenities)}</p>`
  ];

  placeDetails.innerHTML = lines.join("");
}

function renderReviews(reviews) {
  reviewsList.textContent = "";

  if (!reviews.length) {
    message.textContent = "No reviews yet for this place.";
    message.className = "message";
    return;
  }

  message.textContent = "";

  for (const review of reviews) {
    const card = document.createElement("article");
    card.className = "review-card";

    const comment = document.createElement("p");
    comment.textContent = review.text || review.comment || "No comment";

    const header = document.createElement("div");
    header.className = "review-header";

    const user = document.createElement("h4");
    user.textContent = review.user?.name || review.user?.first_name || "Anonymous";

    const rating = document.createElement("span");
    const score = Number(review.rating ?? review.stars ?? 0);
    rating.textContent = `Rating: ${Number.isNaN(score) ? "N/A" : score}/5`;

    header.append(user, rating);
    card.append(header, comment);
    reviewsList.appendChild(card);
  }
}

function setError(text) {
  message.textContent = text;
  message.className = "message error";
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
