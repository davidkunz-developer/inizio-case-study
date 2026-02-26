# Požadavky na aplikaci: Fleet Analytics & Eco-driving Dashboard

## 1. Cíl projektu
Vytvořit interaktivní webovou aplikaci (dashboard) nad veřejným API GPS Dozor. Aplikace bude sloužit správcům vozového parku (fleet managerům) k analýze využití vozidel, sledování chování řidičů a generování přehledů o ujetých kilometrech (kniha jízd). Cílem je poskytnout reálnou hodnotu skrze optimalizaci provozu a ekologičtější jízdu.

## 2. Cílová skupina (Persony)
- **Fleet Manager:** Potřebuje mít přehled o stavu vozového parku, efektivitě využití vozidel, spotřebě a chování řidičů. Hledá příležitosti ke snížení nákladů a bezpečnější jízdu.

## 3. Klíčové funkce (Features)
- **Výběr skupiny a vozidla:** Uživatel může zvolit skupinu vozidel a vybrat konkrétní vozidlo k analýze.
- **Kniha jízd (Log Book):** Pro zvolené časové období se zobrazí přehled všech jízd vybraného vozidla, včetně ujeté vzdálenosti, doby trvání, průměrné rychlosti a spotřeby.
- **Agregace a vizualizace:** Dashboard bude obsahovat grafické znázornění agregovaných ujetých kilometrů po dnech, díky čemuž bude hned jasné časové vytížení vozidla.
- **Eco-driving analýza:** Zobrazení rizikových nebo neekologických událostí (prudké brzdění, zrychlování, řezání zatáček). Tyto eventy budou moci být zobrazeny chronologicky v souvislosti s knihou jízd.
- **Vizualizace a filtrování:**
  - Možnost definovat si analyzované období (date picker).
  - Přehledné tabulky s možností interakce.

## 4. Technické požadavky (API endpointy)
Aplikace splní požadavek testu (využití min. 3 endpointů API):
1. `GET /api/v1/groups` - Získání skupin (Rights/Access management).
2. `GET /api/v1/vehicles/group/<group code>` - Získání seznamu vozidel ve skupině.
3. `GET /api/v1/vehicle/<vehicle code>/trips` - Záznamy historických jízd (Kniha jízd).
4. `GET /api/v1/vehicle/<vehicle code>/eco-driving-events` - Data o ekologické/nebezpečné jízdě.

*Bonusově lze endpointy rozšířit např. o zobrazení aktuální nebo minulé pozice vozidla přes mapové API, pokud se tak rozhodneme v design/dev fázi.*

## 5. Očekávaný přínos
- Rychlá identifikace neefektivně využívaných vozidel.
- Transparentní základna pro optimalizaci jízdy z hlediska bezpečnosti a ESG (snížení emisí skrze lepší způsob řízení).
- Pěkné a ukázkové vizuální zpracování API dat (jádro use casu pro daný pohovor).
