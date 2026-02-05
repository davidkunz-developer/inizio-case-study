import pandas as pd
from io import BytesIO
from fastapi import APIRouter, Response
from app.models.search import SearchResponse

router = APIRouter()


@router.post("/export/excel")
async def export_to_excel(data: SearchResponse):
    results_data = [result.model_dump() for result in data.results]
    
    df = pd.DataFrame(results_data)
    
    df = df.rename(columns={
        "position": "Pozice",
        "title": "Titulek",
        "url": "URL",
        "snippet": "Popis"
    })
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Výsledky')
        
    output.seek(0)
    
    filename = f"search_results_{data.fetched_at.strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return Response(
        content=output.getvalue(),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers=headers
    )
