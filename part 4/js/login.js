import { apiRequest } from "./api.js";
import { isAuthenticated, setTokenCookie } from "./auth.js";

const loginForm = document.getElementById("login-form");
const message = document.getElementById("message");

if (isAuthenticated()) {
  window.location.href = "index.html";
}

loginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";
  message.className = "message";

  const formData = new FormData(loginForm);
  const email = String(formData.get("email") || "").trim();
  const password = String(formData.get("password") || "").trim();

  if (!email || !password) {
    message.textContent = "Email and password are required.";
    message.classList.add("error");
    return;
  }

  try {
    const loginPayload = {
      method: "POST",
      body: JSON.stringify({ email, password })
    };

    let response;
    try {
      response = await apiRequest("/users/login", loginPayload);
    } catch (firstError) {
      try {
        response = await apiRequest("/auth/login", loginPayload);
      } catch (secondError) {
        response = await apiRequest("/login", loginPayload);
      }
    }

    const token =
      response.access_token ||
      response.token ||
      response.jwt ||
      response.data?.access_token ||
      "";
    if (!token) {
      throw new Error("Authentication token missing in response.");
    }

    setTokenCookie(token);
    message.textContent = "Login successful. Redirecting...";
    message.classList.add("success");

    window.setTimeout(() => {
      window.location.href = "index.html";
    }, 300);
  } catch (error) {
    message.textContent = error.message || "Unable to login.";
    message.classList.add("error");
  }
});
