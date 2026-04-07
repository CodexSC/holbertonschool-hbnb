const TOKEN_COOKIE = "hbnb_token";
const ONE_DAY_IN_SECONDS = 60 * 60 * 24;

export function setTokenCookie(token) {
  const cookieParts = [
    `${TOKEN_COOKIE}=${encodeURIComponent(token)}`,
    `max-age=${ONE_DAY_IN_SECONDS}`,
    "path=/",
    "samesite=lax"
  ];

  if (location.protocol === "https:") {
    cookieParts.push("secure");
  }

  document.cookie = cookieParts.join("; ");
}

export function getTokenCookie() {
  const allCookies = document.cookie ? document.cookie.split("; ") : [];

  for (const cookie of allCookies) {
    const [name, value] = cookie.split("=");
    if (name === TOKEN_COOKIE) {
      return decodeURIComponent(value || "");
    }
  }

  return "";
}

export function clearTokenCookie() {
  document.cookie = `${TOKEN_COOKIE}=; max-age=0; path=/; samesite=lax`;
}

export function isAuthenticated() {
  return Boolean(getTokenCookie());
}

export function requireAuth(redirectPath) {
  if (!isAuthenticated()) {
    window.location.href = redirectPath;
    return false;
  }

  return true;
}

export function bindLogout(buttonSelector) {
  const logoutButton = document.querySelector(buttonSelector);
  if (!logoutButton) {
    return;
  }

  logoutButton.addEventListener("click", (event) => {
    event.preventDefault();
    clearTokenCookie();
    window.location.href = "login.html";
  });
}
