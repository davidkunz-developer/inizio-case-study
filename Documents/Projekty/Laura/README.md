# Laura - AI Asistentka Davida Kunze

AI asistentka pro poskytování informací o Davidovi a domlouvání schůzek.

## Funkce

- **Informace o Davidovi**: Odpovídá na dotazy týkající se profesního profilu
- **Domlouvání schůzek**: Pomáhá s plánováním a domlouváním schůzek

## Požadavky

- Python 3.11+
- OpenAI API klíč

## Instalace

1. Klonujte repozitář
2. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

3. Vytvořte soubor `.env` s OpenAI API klíčem:
```
OPENAI_API_KEY=your_api_key_here
```

## Spuštění lokálně

```bash
python api.py
```

Aplikace poběží na `http://localhost:8021`

## Nasazení

### Docker

```bash
docker build -t laura .
docker run -p 8021:8021 --env-file .env laura
```

### Railway / Render / Heroku

1. Připojte GitHub repozitář
2. Nastavte environment variable `OPENAI_API_KEY`
3. Deploy automaticky proběhne

### VPS (Ubuntu/Debian)

1. Nainstalujte Python a pip
2. Klonujte repozitář
3. Vytvořte systemd service nebo použijte supervisor
4. Nastavte reverse proxy (nginx) pro port 8021

## Struktura projektu

- `api.py` - FastAPI backend s LangGraph workflow
- `prompts.py` - Prompt definice pro LLM
- `resume.json` - Strukturovaný životopis Davida
- `static/index.html` - Frontend chat rozhraní

## Technologie

- FastAPI
- LangChain + LangGraph
- OpenAI GPT-4o
- Uvicorn
