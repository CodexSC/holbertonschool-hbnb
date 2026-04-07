import { apiRequest } from "./api.js";
import { getTokenCookie, requireAuth } from "./auth.js";

const form = document.getElementById("review-form");
const message = document.getElementById("message");

if (!requireAuth("index.html")) {
  throw new Error("User must be logged in.");
}

const params = new URLSearchParams(window.location.search);
const placeId = params.get("place_id");

if (!placeId) {
  message.textContent = "Missing place id in URL."
  message.className = "message error";
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";
  message.className = "message";

  if (!placeId) {
    message.textContent = "Missing place id."
    message.classList.add("error");
    return;
  }

  const formData = new FormData(form);
  const rating = Number(formData.get("rating") || 0);
  const comment = String(formData.get("comment") || "").trim();

  if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
    message.textContent = "Rating must be an integer between 1 and 5.";
    message.classList.add("error");
    return;
  }

  if (!comment) {
    message.textContent = "Comment is required.";
    message.classList.add("error");
    return;
  }

  try {
    const token = getTokenCookie();

    try {
      await apiRequest(`/places/${encodeURIComponent(placeId)}/reviews`, {
        method: "POST",
        body: JSON.stringify({ text: comment, rating })
      }, token);
    } catch (error) {
      await apiRequest("/reviews", {
        method: "POST",
        body: JSON.stringify({ place_id: placeId, text: comment, rating })
      }, token);
    }

    message.textContent = "Review added successfully. Redirecting...";
    message.classList.add("success");

    window.setTimeout(() => {
      window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
    }, 450);
  } catch (error) {
    message.textContent = error.message || "Could not add review.";
    message.classList.add("error");
  }
});
