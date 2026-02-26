# Architektura Systému: Fleet Analytics & Eco-driving Dashboard

## 1. Technologický Stack
Vzhledem k požadavkům zadání (Vue.js je plus, veřejné API, frontend-only fokus) navrhuji následující stack:
- **Frontend Framework:** Vue 3 (Composition API) + Vite pro rychlý vývoj a build.
- **Styling:** Tailwind CSS - pro rychlou, moderní a dynamickou tvorbu UI.
- **Stav aplikace (State Management):** Pinia.
- **Data Fetching:** Axios nebo nativní Fetch API.
- **Vizualizace a grafy:** Chart.js (přes `vue-chartjs`) nebo alternativně ECharts pro interaktivní vykreslování dat.
- **Mapové podklady:** Leaflet (přes `vue-leaflet`) pro zobrazení událostí (Eco-driving) a pozic vozidel na mapě.
- **Routování:** Vue Router (pokud bude potřeba více obrazovek, i když se nabízí vše řešit v moderním Single Page Dashboardu bez nutnosti silného routování).

## 2. High-Level Architektura
Aplikace bude postavena primárně jako **Client-Side Rendering (CSR)** SPA (Single Page Application). Data budou stahována z klientského prohlížeče přímo do GPS Dozor API.
*Poznámka: Pokud API nepodporuje Cross-Origin Resource Sharing (CORS) z prohlížeče mimo `gpsguard.eu`, bude nezbytné nakonfigurovat Vite Development Proxy pro lokální vývoj a pro produkci přidat jednoduchý Node.js / Vercel serverless proxy ovladač. Prozatím předpokládáme přímý přístup.*

### 2.1 Adresářová struktura (Návrh konvence)
```text
src/
├── assets/             # Statické soubory, obrázky, globální CSS
├── components/         # Znovupoužitelné UI komponenty
│   ├── VehicleSelect.vue      # Výběr flotily a vozidla
│   ├── LogBookTable.vue       # Tabulka - Kniha jízd
│   ├── EcoEventMap.vue        # Mapa pro Eco-driving
│   └── MileageChart.vue       # Graf kilometrů (Chart.js)
├── composables/        # Znovupoužitelná Vue logika (např. useApi.js)
├── services/           # Služby pro komunikaci s API (axios instance apod.)
├── stores/             # Pinia stores (např. fleetStore.js, vehicleStore.js)
├── views/              # Hlavní stránky aplikací (Dashboard.vue)
├── App.vue
└── main.js
```

## 3. Komunikace komponent
1. Uživatel otevře `Dashboard`. Komponenta přes `fleetStore` získá dostupné skupiny a naplní jimi `VehicleSelect`.
2. Při výběru skupiny se načtou vozidla v této skupině.
3. Po výběru vozidla uživatelem je ID vozidla nastaveno ve store coby `activeVehicle`.
4. Komponenty pro zobrazení (`LogBookTable`, `MileageChart`, `EcoEventMap`) reaktivně detekují změnu `activeVehicle` a zavolají data layer service (`services/api.js`) pro stažení specifik (trips, eco-driving events).
5. Data se vykreslí a nabídnou interaktivní tooltipy a animace (Tailwind/CSS transitions) pro prémiový "Vibe Coder" vzhled.
