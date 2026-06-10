document.addEventListener("DOMContentLoaded", () => {
  const mapEl = document.getElementById("map");
  const adresseInput = document.getElementById("adresse");
  const villeInput = document.getElementById("ville");
  const codePostalInput = document.getElementById("code_postal");
  const departementSelect = document.getElementById("code_departement");
  const latInput = document.getElementById("latitude");
  const lngInput = document.getElementById("longitude");
  const suggestionsBox = document.getElementById("address-suggestions");
  const mapHint = document.getElementById("map-hint");

  if (!mapEl) return;

  let departements = {};
  try {
    departements = JSON.parse(mapEl.dataset.departements || "{}");
  } catch (err) {
    console.error("Impossible de lire les départements :", err);
  }

  const initialLat = parseFloat(mapEl.dataset.lat) || 46.603354;
  const initialLng = parseFloat(mapEl.dataset.lng) || 1.888334;

  const map = L.map("map").setView([initialLat, initialLng], (mapEl.dataset.lat && mapEl.dataset.lng) ? 14 : 6);

  window.map = map;

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  let marker = null;
  window.marker = marker;

  function setMarker(lat, lng) {
    if (marker) {
      marker.setLatLng([lat, lng]);
    } else {
      marker = L.marker([lat, lng]).addTo(map);
      window.marker = marker;
    }
    map.setView([lat, lng], 15);
  }

  function extractDepartmentFromContext(context) {
    if (!context) return "";
    const first = context.split(",")[0]?.trim() || "";
    return first;
  }

  function updateLocationFields({ lat, lng, postcode = "", city = "", label = "", department = "" }) {
    latInput.value = lat;
    lngInput.value = lng;

    if (postcode && !codePostalInput.value) codePostalInput.value = postcode;
    if (city && !villeInput.value) villeInput.value = city;
    if (label) adresseInput.value = label;

    if (department && departementSelect.querySelector(`option[value="${department}"]`)) {
      departementSelect.value = department;
    }

    setMarker(lat, lng);
    if (mapHint) {
      mapHint.textContent = "Position sélectionnée. Vous pouvez encore déplacer le point sur la carte si besoin.";
    }
  }

  if (mapEl.dataset.lat && mapEl.dataset.lng) {
    setMarker(parseFloat(mapEl.dataset.lat), parseFloat(mapEl.dataset.lng));
  }

  map.on("click", async (e) => {
    const lat = e.latlng.lat.toFixed(6);
    const lng = e.latlng.lng.toFixed(6);

    latInput.value = lat;
    lngInput.value = lng;
    setMarker(lat, lng);

    if (mapHint) {
      mapHint.textContent = "Point placé sur la carte. Tentative de récupération automatique de l'adresse...";
    }

    try {
      const url = `https://api-adresse.data.gouv.fr/reverse/?lon=${lng}&lat=${lat}`;
      const res = await fetch(url);
      const data = await res.json();

      if (data.features && data.features.length > 0) {
        const item = data.features[0];
        const props = item.properties || {};
        const dept = extractDepartmentFromContext(props.context);

        adresseInput.value = props.label || adresseInput.value;
        villeInput.value = props.city || villeInput.value;
        codePostalInput.value = props.postcode || codePostalInput.value;

        if (dept && departementSelect.querySelector(`option[value="${dept}"]`)) {
          departementSelect.value = dept;
        }

        if (mapHint) {
          mapHint.textContent = "Adresse récupérée depuis la carte.";
        }
      } else if (mapHint) {
        mapHint.textContent = "Point placé sur la carte. Adresse non trouvée automatiquement.";
      }
    } catch (err) {
      console.error(err);
      if (mapHint) {
        mapHint.textContent = "Point placé sur la carte. Erreur lors de la recherche d'adresse.";
      }
    }
  });

  let debounceTimer = null;

  async function searchAddress() {
    const adresse = adresseInput.value.trim();
    const ville = villeInput.value.trim();
    const cp = codePostalInput.value.trim();

    const q = [adresse, cp, ville].filter(Boolean).join(" ").trim();
    if (q.length < 3) {
      suggestionsBox.classList.add("hidden");
      suggestionsBox.innerHTML = "";
      return;
    }

    const params = new URLSearchParams({
      q,
      limit: 6,
      autocomplete: 1
    });

    if (cp) params.append("postcode", cp);

    try {
      const res = await fetch(`https://api-adresse.data.gouv.fr/search/?${params.toString()}`);
      const data = await res.json();

      suggestionsBox.innerHTML = "";

      if (!data.features || data.features.length === 0) {
        suggestionsBox.classList.add("hidden");
        return;
      }

      data.features.forEach((feature) => {
        const props = feature.properties || {};
        const coords = feature.geometry?.coordinates || [];
        const department = extractDepartmentFromContext(props.context);

        const div = document.createElement("div");
        div.className = "suggestion-item";
        div.textContent = props.label || "Adresse";
        div.addEventListener("click", () => {
          updateLocationFields({
            lat: coords[1],
            lng: coords[0],
            postcode: props.postcode || "",
            city: props.city || "",
            label: props.label || "",
            department
          });
          suggestionsBox.classList.add("hidden");
          suggestionsBox.innerHTML = "";
        });

        suggestionsBox.appendChild(div);
      });

      suggestionsBox.classList.remove("hidden");
    } catch (err) {
      console.error("Erreur autocomplétion adresse :", err);
      suggestionsBox.classList.add("hidden");
      suggestionsBox.innerHTML = "";
    }
  }

  [adresseInput, villeInput, codePostalInput].forEach((input) => {
    input.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(searchAddress, 300);
    });
  });

  document.addEventListener("click", (e) => {
    if (!suggestionsBox.contains(e.target) && e.target !== adresseInput && e.target !== villeInput && e.target !== codePostalInput) {
      suggestionsBox.classList.add("hidden");
    }
  });
});