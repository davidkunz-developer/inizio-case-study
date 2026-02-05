import httpx
from fastapi import APIRouter, HTTPException, Query
from app.services.search_service import SearchService
from app.models.search import SearchResponse

router = APIRouter()
search_service = SearchService()


@router.get("/search", response_model=SearchResponse)
async def search(user_input: str = Query(..., min_length=1)):
    if not user_input or not user_input.strip():
        raise HTTPException(status_code=400, detail="Vyhledávací dotaz nesmí být prázdný")
    
    try:
        return search_service.search(user_input.strip())
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            detail = "Neplatný API klíč pro vyhledávací službu."
        elif e.response.status_code == 402:
            detail = "Limit vyhledávání pro tento měsíc byl vyčerpán."
        elif e.response.status_code == 429:
            detail = "Příliš mnoho požadavků najednou. Zkuste to prosím za chvíli."
        else:
            detail = f"Chyba vyhledávací služby: {e.response.status_code}"
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Vyhledávací služba neodpověděla včas. Zkuste to prosím znovu.")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Vyhledávací služba je momentálně nedostupná (problém s připojením).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neočekávaná chyba: {str(e)}")
