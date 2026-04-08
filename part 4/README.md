# HBnB Frontend - Part 4

A modular, vanilla JavaScript frontend for HBnB that connects to a REST API and delivers:
- authentication with JWT cookies
- dynamic place listing with client-side price filtering
- place details with amenities and reviews
- authenticated review submission

The UI design follows a cohesive identity across all pages: warm rose/crimson palette, glass-like surfaces, rounded cards, and subtle motion.

---

## 1) Project Overview

This project is a static frontend application (HTML/CSS/JavaScript modules) that communicates with the backend API at:

- http://127.0.0.1:5000/api/v1

Main user journeys:
- Sign in from Login page
- Browse places on Index page
- Filter places instantly by max price
- Open a place details page
- Submit a review (authenticated users only)

---

## 2) Visual Identity and Aesthetic Direction

The interface keeps a consistent visual system across pages:

- Typography:
  - Manrope (UI body)
  - Space Grotesk (headlines)
- Color style:
  - warm rose backgrounds
  - crimson accents for actions
  - soft translucent cards
- Motion:
  - fade-in page load
  - card rise effects on entry
  - hover lift and shadow transitions

This preserves cohesion between login, listing, details, and review workflows.

---

## 3) Workspace Structure

```text
part 4/
├── README.md
├── index.html
├── login.html
├── place.html
├── add_review.html
├── styles.css
├── favicon-96x96.png
├── favicon/
│   └── site.webmanifest
└── js/
    ├── api.js
    ├── auth.js
    ├── login.js
    ├── index.js
    ├── place.js
    └── add_review.js
```

---

## 4) Schematics

### 4.1 Page and Navigation Map

```text
                +----------------+
                |   login.html   |
                |   (login.js)   |
                +-------+--------+
                        |
                        | successful auth -> set JWT cookie
                        v
+----------------+  +---+----------------+   click place card   +----------------+
| add_review.html|<-|    index.html      |--------------------->|   place.html   |
| (add_review.js)|  |    (index.js)      |                      |   (place.js)   |
+--------+-------+  +---------+----------+                      +--------+-------+
         ^                    |                                           |
         |                    | load places + price filter                |
         |                    +-------------------------------------------+
         |                                  view details + reviews
         |
         +-------------- authenticated users only ------------------------+
```

### 4.2 Authentication State Schematic

```text
[Page load]
    |
    v
Read token cookie (token)
    |
    +--> token missing:
    |       - show Login link
    |       - hide Logout link
    |       - redirect to index for add_review page
    |
    +--> token present:
            - hide Login link
            - show Logout link
            - add Authorization: Bearer <token> to API requests
            - allow add-review access
```

### 4.3 Data Flow Schematic

```text
UI Event -> JS Module -> apiRequest() -> Backend API -> JSON Payload -> DOM Render

Examples:
- Submit Login Form -> login.js -> POST /users/login (fallbacks) -> token -> cookie saved
- Index Load -> index.js -> GET /places -> place cards rendered
- Price Change -> index.js -> client-side filter (no reload)
- Place Load -> place.js -> GET /places/:id + reviews endpoint -> details and reviews rendered
- Submit Review -> add_review.js -> POST /places/:id/reviews (fallback /reviews) -> success message
```

### 4.4 Endpoint Matrix

| Purpose | Primary Endpoint | Fallback Endpoint | Auth |
|---|---|---|---|
| Login | POST /users/login | POST /auth/login, POST /login | No |
| List places | GET /places | - | Optional |
| Place details | GET /places/:id | - | Optional |
| Place reviews | GET /places/:id/reviews | GET /reviews?place_id=:id | Optional |
| Add review | POST /places/:id/reviews | POST /reviews | Yes |

---

## 5) Implementation Details by Module

### 5.1 js/api.js

Central request utility:
- stores API base URL
- sets Content-Type: application/json
- injects Authorization header when token exists
- normalizes error handling from response payload
- returns parsed JSON (or null for 204)

Why this matters:
- avoids duplicated fetch logic
- enforces consistent API behavior and error formatting

### 5.2 js/auth.js

Authentication helper module:
- setTokenCookie(token)
- getTokenCookie()
- clearTokenCookie()
- isAuthenticated()
- requireAuth(redirectPath)
- bindLogout(selector)

Cookie strategy:
- max-age: 1 day
- path: /
- samesite: lax
- secure flag only on HTTPS

### 5.3 login.html + js/login.js

Responsibilities:
- show login form
- prevent re-login if already authenticated
- submit credentials
- parse token from multiple backend response shapes
- persist JWT in cookie and redirect to index

Resilience:
- tries multiple login routes to support backend variations

### 5.4 index.html + js/index.js

Responsibilities:
- fetch all places
- render place cards dynamically
- provide instant client-side max-price filtering
- toggle Login/Logout visibility by auth state

Filter behavior:
- options: All, 10, 50, 100
- implemented in-browser with display toggling
- no additional API calls

### 5.5 place.html + js/place.js

Responsibilities:
- read place id from query string
- fetch and render detailed place info
- fetch and render associated reviews
- reveal Add Review access only for authenticated users
- set Add Review link with place_id parameter

Displayed detail fields:
- name
- host
- price per night
- description
- amenities
- reviews list

### 5.6 add_review.html + js/add_review.js

Responsibilities:
- enforce authentication (redirect unauthenticated users)
- read place_id from URL
- validate rating and comment input
- submit review payload to API
- show success/error message and reset form on success

Submission compatibility:
- primary post to /places/:id/reviews
- fallback post to /reviews

---

## 6) Runtime and Setup

### 6.1 Prerequisites

- Running HBnB backend API at http://127.0.0.1:5000
- Browser with JavaScript enabled

### 6.2 Run Locally

Serve the folder as static files (example):

```bash
cd "part 4"
python3 -m http.server 8000
```

Then open:
- http://127.0.0.1:8000/login.html
- http://127.0.0.1:8000/index.html

---

## 7) Manual Test Plan

### Login
- Open login page
- Submit valid credentials
- Confirm token cookie is created
- Confirm redirect to index

### Index
- Confirm places load from API
- Confirm login/logout visibility updates with auth state
- Change max-price filter and verify cards show/hide instantly

### Place Details
- Open place.html?id=<valid_place_id>
- Confirm detailed fields render
- Confirm reviews load
- Confirm add-review section appears only when authenticated

### Add Review
- Open add_review.html?place_id=<valid_place_id>
- If not authenticated, confirm redirect to index
- Submit valid review and verify success message
- Submit invalid rating/comment and verify validation errors

---

## 8) Error Handling Strategy

The project uses defensive handling at three levels:

1. Input validation
- required fields (email/password/comment)
- rating integer range [1..5]
- required place ids in URL

2. API response safety
- non-OK status converted to Error with payload message
- support for varied payload wrappers: raw arrays, results, data

3. UX feedback
- in-page message blocks for success/error
- clear text on missing params and failed requests

---

## 9) Extension Guide

Potential next improvements:

- Add user registration page and module
- Add loading skeletons and retry actions
- Add pagination for large place lists
- Add sort controls (price ascending/descending)
- Add richer review metadata (date/user avatar)
- Add end-to-end tests for key user journeys

---

## 10) Credits

HBnB Frontend - Holberton School project, Part 4.

Designed and implemented as a clean, modular, API-driven client with a cohesive visual language.
