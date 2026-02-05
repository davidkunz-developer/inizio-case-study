import pandas as pd
from io import BytesIO
from datetime import datetime
from fastapi import APIRouter, Response, HTTPException
from app.models.search import SearchResponse

router = APIRouter()


@router.post("/export/excel")
async def export_to_excel(data: SearchResponse):
    try:
        if not data.results:
            raise HTTPException(status_code=400, detail="Nejsou k dispozici žádné výsledky pro export.")

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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chyba při generování Excelu: {str(e)}")
