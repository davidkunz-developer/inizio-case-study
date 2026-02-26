# API Kontrakt: GPS Dozor Fleet Dashboard

Tento dokument mapuje, jak budou data z poskytnutého dodavatelského API GPS Dozor proudit do naší frontend aplikace. Aplikace použije základní base URL: `https://a1.gpsguard.eu/api/v1`

## 1. Výběr skupiny a vozidla
**Endpoint:** `GET /groups`
- **Účel:** Získat práva a identifikátory (GroupCode) dostupných skupin.
- **Aplikace:** Výběr počáteční fleet struktury v našem Dropdownu nebo sidebaru.
- **Odpověď:** Array of `{ "Code": string, "Name": string }`

**Endpoint:** `GET /vehicles/group/{groupCode}`
- **Účel:** Získat seznam vozidel a jejich základní informace pro vybranou skupinu (SPZ, základní stav baterie, počítadlo ujeté vzdálenosti, apod.).
- **Aplikace:** Master-detail list vozidel. Odpověď parsujeme pro extrakt `Code` (slouží dále jako `vehicle code`), `Name` a `SPZ`.

## 2. Kniha Jízd (Log Book) & Vytíženost vozidla (Graf)
**Endpoint:** `GET /vehicle/{vehicleCode}/trips?from={datetime}&to={datetime}`
- **Parametry:** `from` a `to` v ISO/UTC formátu (např. `2021-03-01T00:00`). Backend-Dev / Frontend-Dev zajistí vytvoření date pickeru na UI, default bude posledních 7 - 30 dní.
- **Účel:** Kniha jízd pro detail vozidla.
- **Aplikace:**
  - Tabulka zobrazí položky: `StartTime`, `FinishTime`, `TotalDistance`, `AverageSpeed` a `MaxSpeed`.
  - Agregace do Bar/Line Chart (např. zkompilujeme na frontendu ujeté dny z polí `StartTime` a sečteme `TotalDistance` pro jednotlivé dny).

## 3. Detekce Eco-drivingu na mapě a analýze rizik
**Endpoint:** `GET /vehicle/{vehicleCode}/eco-driving-events?from={datetime}&to={datetime}`
- **Účel:** Vyhledání hard braking, ostrého zatáčení s cílem postavit Eco-driving risk metriku.
- **Datové parametry k extrakci:**
  - `EventType`: Kódy od 0 do 9 (Acceleration, Braking, Cornering, atd.).
  - `Position`: Mapování `{ "Latitude", "Longitude" }` do mapových pinů (Leaflet).
  - `EventSeverity`: Kódy Low, Medium, High pro barvení pinu/události (žlutá, oranžová, červená).

## 4. Očekávané výzvy (Risks & Mitigations)
- **Autentizace:** Autentizace momentálně není explicitně specifikována z hlediska tokenů pro "GPS Dozor API" v dokumentaci. Předpoklad je, že použijeme cookie based auth, nebo pro test jsou endpointy veřejné. (TODO Frontend-Dev k namapování a prozkoumání `GET /groups`).
- **CORS Errors:** V případě 403 / CORS u Vite dev serveru použít plugin:
```js
// vite.config.js proxy
export default defineConfig({
  server: { proxy: { '/api': { target: 'https://a1.gpsguard.eu', changeOrigin: true } } }
})
```
Pokyn pro Frontend-Dev: Architektura i kontrakt jsou schváleny a můžete přistoupit k implementaci. Vše musí běžet a dávat WOW uživatelský efekt, dynamický a fresh design.
