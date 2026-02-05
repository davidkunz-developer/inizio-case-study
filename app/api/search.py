from fastapi import APIRouter, HTTPException, Query
from app.services.search_service import SearchService
from app.models.search import SearchResponse

router = APIRouter()
search_service = SearchService()


@router.get("/search", response_model=SearchResponse)
async def search(user_input: str = Query(..., min_length=1)):
    if not user_input or not user_input.strip():
        raise HTTPException(status_code=400, detail="Vyhledávací dotaz nesmí být prázdný")
    
    return search_service.search(user_input.strip())
