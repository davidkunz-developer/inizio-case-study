# Inizio Case Study - Google Search API

Jednoduchá webová aplikace, která prohledává Google (pomocí SerpAPI), zobrazuje organické výsledky a umožňuje jejich export.

## Funkce
- Vyhledávání na Google (pouze organické výsledky)
- Čisté a jednoduché HTML rozhraní
- Export výsledků do JSON
- Export výsledků do Excelu (.xlsx)

## Architektura
```
frontend (HTML/JS) → FastAPI backend → SearchService → SerpAPI → Frontend
```

## Požadavky
- Python 3.11+
- API klíč ze [SerpAPI](https://serpapi.com/) (zdarma)

## Instalace

1. Vytvořte virtuální prostředí (volitelné, ale doporučené):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

3. Nastavte API klíč:
   - Zkopírujte `.env.example` na `.env`
   - Vložte svůj `SERPAPI_API_KEY` do souboru `.env`

## Spuštění (Lokálně)

```bash
uvicorn app.main:app --reload
```
Aplikace poběží na: http://localhost:8000

## Spuštění (Docker)

```bash
docker-compose up --build
```

## Testování

Projekt obsahuje unit testy pro vyhledávání i export.

```bash
pytest tests/ -v
```

### Seznam unit testů

| Název testu | Oblast | Co přesně ověřuje |
| :--- | :--- | :--- |
| `test_search_returns_search_response` | Vyhledávání | Zda služba vrací správný objekt `SearchResponse`. |
| `test_search_response_has_correct_structure` | Vyhledávání | Přítomnost všech povinných polí v odpovědi (datum, zdroj, výsledky). |
| `test_search_results_are_search_result_instances` | Vyhledávání | Správné formátování každého jednotlivého výsledku (SearchResult). |
| `test_search_result_positions_are_sequential` | Vyhledávání | Zachování správného pořadí pozic (1, 2, 3...) z výsledků Googlu. |
| `test_total_returned_matches_results_length` | Vyhledávání | Soulad mezi nahlášeným počtem výsledků a skutečnou délkou seznamu. |
| `test_fetched_at_is_utc` | Vyhledávání | Zajištění, že čas vyhledávání je vždy v mezinárodním formátu UTC. |
| `test_parse_organic_results_with_empty_items` | Odolnost | Bezpečné zpracování situace, kdy Google nevrátí žádné výsledky. |
| `test_parse_organic_results_with_missing_key` | Odolnost | Stabilita parsování v případě, že JSON od API má neočekávanou strukturu. |
| `test_parse_organic_results_with_valid_data` | Odolnost | Správný převod surového JSONu na vyčištěný seznam výsledků. |
| `test_parse_organic_results_with_missing_snippet` | Odolnost | Funkčnost aplikace i v případě, že u výsledku chybí popisek (snippet). |
| `test_export_excel_endpoint` | Export | Schopnost backendu vygenerovat a poslat Excel soubor ke stažení. |

## Odolnost a ošetření chyb

Aplikace je navržena s důrazem na stabilitu a uživatelskou zkušenost (UX). Implementuje mechanismus **Graceful Degradation**:

- **Automatický Fallback:** Pokud selže komunikace s externím API (např. vyčerpaný limit, neplatný klíč nebo výpadek sítě), aplikace automaticky přepne do demo režimu a zobrazí lokální ukázková data.
- **Informativní hlášky:** Uživatel je o každém problému informován prostřednictvím vizuálních upozornění přímo v rozhraní (např. "Limit vyhledávání vyčerpán - zobrazuji ukázková data").
- **Timeouts:** Po 10 sekundách nečinnosti externího API aplikace automaticky ukončí čekání a přejde k náhradnímu řešení.
- **Validace:** Veškeré vstupy i exporty jsou validovány, aby se předešlo neočekávaným pádům systému.

## Struktura projektu
```
app/
  api/          # API endpointy
  models/       # Pydantic modely
  services/     # Business logika (SerpAPI integrace)
  static/       # Frontend (HTML, CSS, JS)
  main.py       # Hlavní aplikace
tests/          # Unit testy
```
