const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

export async function apiRequest(path, options = {}, token = null) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {})
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    let payload = null;

    try {
      payload = await response.json();
    } catch (error) {
      payload = null;
    }

    const message = payload?.error || payload?.message || `Request failed (${response.status})`;
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
