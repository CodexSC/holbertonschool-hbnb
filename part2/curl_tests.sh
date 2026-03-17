#!/bin/bash
# ============================================================
# HBnB API – Tests cURL manuels
# Démarrer le serveur avant : python run.py
# URL : http://127.0.0.1:5000
# ============================================================

BASE="http://127.0.0.1:5000/api/v1"

echo "========================================"
echo "  USERS"
echo "========================================"

echo ""
echo "--- [1] Créer un utilisateur (succès → 201) ---"
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"secret123","first_name":"Alice","last_name":"Smith"}' \
  | python3 -m json.tool

echo ""
echo "--- [2] Créer un utilisateur - email manquant (erreur → 400) ---"
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"password":"secret123","first_name":"Alice","last_name":"Smith"}' \
  | python3 -m json.tool

echo ""
echo "--- [3] Créer un utilisateur - email invalide sans domaine (erreur → 400) ---"
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"invalidemail","password":"secret123","first_name":"Alice","last_name":"Smith"}' \
  | python3 -m json.tool

echo ""
echo "--- [4] Créer un utilisateur - email invalide sans TLD (erreur → 400) ---"
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example","password":"secret123","first_name":"Alice","last_name":"Smith"}' \
  | python3 -m json.tool

echo ""
echo "--- [5] Créer un utilisateur - first_name vide (erreur → 400) ---"
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@example.com","password":"secret123","first_name":"","last_name":"Smith"}' \
  | python3 -m json.tool

echo ""
echo "--- [6] Créer un utilisateur - email déjà utilisé (erreur → 409) ---"
curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"autre","first_name":"Alice2","last_name":"Smith2"}' \
  | python3 -m json.tool

echo ""
echo "--- [7] Lister tous les utilisateurs (succès → 200) ---"
curl -s -X GET "$BASE/users/" | python3 -m json.tool

echo ""
echo "--- [8] Récupérer l'utilisateur créé (succès → 200) ---"
USER_ID=$(curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"getme@example.com","password":"secret","first_name":"Get","last_name":"Me"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
curl -s -X GET "$BASE/users/$USER_ID" | python3 -m json.tool

echo ""
echo "--- [9] Récupérer un utilisateur inexistant (erreur → 404) ---"
curl -s -X GET "$BASE/users/00000000-0000-0000-0000-000000000000" | python3 -m json.tool

echo ""
echo "--- [10] Mettre à jour un utilisateur (succès → 200) ---"
curl -s -X PUT "$BASE/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Updated"}' \
  | python3 -m json.tool

echo ""
echo "--- [11] Mettre à jour un utilisateur inexistant (erreur → 404) ---"
curl -s -X PUT "$BASE/users/00000000-0000-0000-0000-000000000000" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Ghost"}' \
  | python3 -m json.tool


echo ""
echo "========================================"
echo "  AMENITIES"
echo "========================================"

echo ""
echo "--- [12] Créer une amenity (succès → 201) ---"
curl -s -X POST "$BASE/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Wi-Fi","description":"Haut débit"}' \
  | python3 -m json.tool

echo ""
echo "--- [13] Créer une amenity - nom vide (erreur → 400) ---"
curl -s -X POST "$BASE/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":""}' \
  | python3 -m json.tool

echo ""
echo "--- [14] Créer une amenity - nom trop long (erreur → 400) ---"
curl -s -X POST "$BASE/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"}' \
  | python3 -m json.tool

echo ""
echo "--- [15] Lister toutes les amenities (succès → 200) ---"
curl -s -X GET "$BASE/amenities/" | python3 -m json.tool

echo ""
echo "--- [16] Récupérer une amenity par ID (succès → 200) ---"
AMENITY_ID=$(curl -s -X POST "$BASE/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Parking"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
curl -s -X GET "$BASE/amenities/$AMENITY_ID" | python3 -m json.tool

echo ""
echo "--- [17] Récupérer une amenity inexistante (erreur → 404) ---"
curl -s -X GET "$BASE/amenities/00000000-0000-0000-0000-000000000000" | python3 -m json.tool

echo ""
echo "--- [18] Mettre à jour une amenity (succès → 200) ---"
curl -s -X PUT "$BASE/amenities/$AMENITY_ID" \
  -H "Content-Type: application/json" \
  -d '{"name":"Parking Couvert"}' \
  | python3 -m json.tool

echo ""
echo "--- [19] Mettre à jour une amenity inexistante (erreur → 404) ---"
curl -s -X PUT "$BASE/amenities/00000000-0000-0000-0000-000000000000" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ghost"}' \
  | python3 -m json.tool


echo ""
echo "========================================"
echo "  PLACES"
echo "========================================"

# Créer owner et amenity pour les tests places
OWNER_ID=$(curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"owner@example.com","password":"secret","first_name":"Owner","last_name":"Test"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

AMENITY2_ID=$(curl -s -X POST "$BASE/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Piscine"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

echo ""
echo "--- [20] Créer un place (succès → 201) ---"
curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Bel Appartement\",\"description\":\"Centre-ville\",\"price\":85.0,\"latitude\":48.85,\"longitude\":2.35,\"owner_id\":\"$OWNER_ID\",\"amenities\":[\"$AMENITY2_ID\"]}" \
  | python3 -m json.tool

echo ""
echo "--- [21] Créer un place - titre vide (erreur → 400) ---"
curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"\",\"description\":\"test\",\"price\":85.0,\"latitude\":48.85,\"longitude\":2.35,\"owner_id\":\"$OWNER_ID\",\"amenities\":[]}" \
  | python3 -m json.tool

echo ""
echo "--- [22] Créer un place - prix nul (erreur → 400) ---"
curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test\",\"description\":\"test\",\"price\":0,\"latitude\":48.85,\"longitude\":2.35,\"owner_id\":\"$OWNER_ID\",\"amenities\":[]}" \
  | python3 -m json.tool

echo ""
echo "--- [23] Créer un place - prix négatif (erreur → 400) ---"
curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test\",\"description\":\"test\",\"price\":-50,\"latitude\":48.85,\"longitude\":2.35,\"owner_id\":\"$OWNER_ID\",\"amenities\":[]}" \
  | python3 -m json.tool

echo ""
echo "--- [24] Créer un place - latitude hors limite (erreur → 400) ---"
curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test\",\"description\":\"test\",\"price\":50,\"latitude\":95.0,\"longitude\":2.35,\"owner_id\":\"$OWNER_ID\",\"amenities\":[]}" \
  | python3 -m json.tool

echo ""
echo "--- [25] Créer un place - longitude hors limite (erreur → 400) ---"
curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test\",\"description\":\"test\",\"price\":50,\"latitude\":48.85,\"longitude\":200.0,\"owner_id\":\"$OWNER_ID\",\"amenities\":[]}" \
  | python3 -m json.tool

echo ""
echo "--- [26] Créer un place - owner inexistant (erreur → 400) ---"
curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"test","price":50,"latitude":48.85,"longitude":2.35,"owner_id":"00000000-0000-0000-0000-000000000000","amenities":[]}' \
  | python3 -m json.tool

echo ""
echo "--- [27] Lister tous les places (succès → 200) ---"
curl -s -X GET "$BASE/places/" | python3 -m json.tool

echo ""
echo "--- [28] Récupérer un place par ID avec owner et amenities (succès → 200) ---"
PLACE_ID=$(curl -s -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Maison Vue Mer\",\"description\":\"Magnifique\",\"price\":120.0,\"latitude\":43.30,\"longitude\":5.37,\"owner_id\":\"$OWNER_ID\",\"amenities\":[\"$AMENITY2_ID\"]}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
curl -s -X GET "$BASE/places/$PLACE_ID" | python3 -m json.tool

echo ""
echo "--- [29] Récupérer un place inexistant (erreur → 404) ---"
curl -s -X GET "$BASE/places/00000000-0000-0000-0000-000000000000" | python3 -m json.tool

echo ""
echo "--- [30] Mettre à jour un place (succès → 200) ---"
curl -s -X PUT "$BASE/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Maison Vue Mer - MAJ\",\"description\":\"Encore plus belle\",\"price\":150.0,\"latitude\":43.30,\"longitude\":5.37,\"owner_id\":\"$OWNER_ID\",\"amenities\":[]}" \
  | python3 -m json.tool

echo ""
echo "--- [31] Mettre à jour un place inexistant (erreur → 404) ---"
curl -s -X PUT "$BASE/places/00000000-0000-0000-0000-000000000000" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Ghost\",\"description\":\"\",\"price\":10,\"latitude\":0,\"longitude\":0,\"owner_id\":\"$OWNER_ID\",\"amenities\":[]}" \
  | python3 -m json.tool


echo ""
echo "========================================"
echo "  REVIEWS"
echo "========================================"

# Créer un reviewer pour les tests
REVIEWER_ID=$(curl -s -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"reviewer@example.com","password":"secret","first_name":"Bob","last_name":"Jones"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

echo ""
echo "--- [32] Créer une review (succès → 201) ---"
curl -s -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"rating\":4,\"comment\":\"Super endroit !\",\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}" \
  | python3 -m json.tool

echo ""
echo "--- [33] Créer une review - commentaire vide (erreur → 400) ---"
curl -s -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"rating\":4,\"comment\":\"\",\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}" \
  | python3 -m json.tool

echo ""
echo "--- [34] Créer une review - note trop basse (erreur → 400) ---"
curl -s -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"rating\":0,\"comment\":\"Bof\",\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}" \
  | python3 -m json.tool

echo ""
echo "--- [35] Créer une review - note trop haute (erreur → 400) ---"
curl -s -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"rating\":6,\"comment\":\"Excellent\",\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}" \
  | python3 -m json.tool

echo ""
echo "--- [36] Créer une review - user inexistant (erreur → 404) ---"
curl -s -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"rating\":3,\"comment\":\"Ok\",\"user_id\":\"00000000-0000-0000-0000-000000000000\",\"place_id\":\"$PLACE_ID\"}" \
  | python3 -m json.tool

echo ""
echo "--- [37] Créer une review - place inexistant (erreur → 404) ---"
curl -s -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"rating\":3,\"comment\":\"Ok\",\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"00000000-0000-0000-0000-000000000000\"}" \
  | python3 -m json.tool

echo ""
echo "--- [38] Lister toutes les reviews (succès → 200) ---"
curl -s -X GET "$BASE/reviews/" | python3 -m json.tool

echo ""
echo "--- [39] Récupérer une review par ID (succès → 200) ---"
REVIEW_ID=$(curl -s -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"rating\":5,\"comment\":\"Parfait !\",\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
curl -s -X GET "$BASE/reviews/$REVIEW_ID" | python3 -m json.tool

echo ""
echo "--- [40] Récupérer une review inexistante (erreur → 404) ---"
curl -s -X GET "$BASE/reviews/00000000-0000-0000-0000-000000000000" | python3 -m json.tool

echo ""
echo "--- [41] Mettre à jour une review (succès → 200) ---"
curl -s -X PUT "$BASE/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{"rating":3,"comment":"Finalement moyen."}' \
  | python3 -m json.tool

echo ""
echo "--- [42] Mettre à jour une review inexistante (erreur → 404) ---"
curl -s -X PUT "$BASE/reviews/00000000-0000-0000-0000-000000000000" \
  -H "Content-Type: application/json" \
  -d '{"rating":3,"comment":"Ghost"}' \
  | python3 -m json.tool

echo ""
echo "--- [43] Récupérer les reviews d'un place (succès → 200) ---"
curl -s -X GET "$BASE/reviews/places/$PLACE_ID/reviews" | python3 -m json.tool

echo ""
echo "--- [44] Récupérer les reviews d'un place inexistant (erreur → 404) ---"
curl -s -X GET "$BASE/reviews/places/00000000-0000-0000-0000-000000000000/reviews" | python3 -m json.tool

echo ""
echo "--- [45] Supprimer une review (succès → 200) ---"
curl -s -X DELETE "$BASE/reviews/$REVIEW_ID" | python3 -m json.tool

echo ""
echo "--- [46] Vérifier que la review supprimée n'existe plus (erreur → 404) ---"
curl -s -X GET "$BASE/reviews/$REVIEW_ID" | python3 -m json.tool

echo ""
echo "--- [47] Supprimer une review inexistante (erreur → 404) ---"
curl -s -X DELETE "$BASE/reviews/00000000-0000-0000-0000-000000000000" | python3 -m json.tool

echo ""
echo "========================================"
echo "  FIN DES TESTS (47 requêtes)"
echo "========================================"
