import { apiRequest } from "./api.js";
import { bindLogout, getTokenCookie } from "./auth.js";

const form = document.getElementById("review-form");
const message = document.getElementById("message");
const loginLink = document.getElementById("login-link");
const logoutLink = document.getElementById("logout-link");

const token = checkAuthentication();

const params = new URLSearchParams(window.location.search);
const placeId = params.get("place_id");

if (!placeId) {
  message.textContent = "Missing place id in URL.";
  message.className = "message error";
}

configureAuthUi();

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";
  message.className = "message";

  if (!placeId) {
    message.textContent = "Missing place id.";
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
    try {
      await submitReviewToPlaceEndpoint(token, placeId, comment, rating);
    } catch (error) {
      await submitReviewToReviewsEndpoint(token, placeId, comment, rating);
    }

    message.textContent = "Review submitted successfully.";
    message.classList.add("success");
    form.reset();
  } catch (error) {
    message.textContent = error.message || "Could not add review.";
    message.classList.add("error");
  }
});

function checkAuthentication() {
  const jwtToken = getTokenCookie();

  if (!jwtToken) {
    window.location.href = "index.html";
    return "";
  }

  return jwtToken;
}

function configureAuthUi() {
  bindLogout("#logout-link");

  if (loginLink) {
    loginLink.style.display = "none";
  }

  if (logoutLink) {
    logoutLink.style.display = "inline-flex";
  }
}

function submitReviewToPlaceEndpoint(jwtToken, id, comment, rating) {
  return apiRequest(
    `/places/${encodeURIComponent(id)}/reviews`,
    {
      method: "POST",
      body: JSON.stringify({ text: comment, rating })
    },
    jwtToken
  );
}

function submitReviewToReviewsEndpoint(jwtToken, id, comment, rating) {
  return apiRequest(
    "/reviews",
    {
      method: "POST",
      body: JSON.stringify({ place_id: id, text: comment, rating })
    },
    jwtToken
  );
}
