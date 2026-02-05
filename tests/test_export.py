import pytest
import pandas as pd
from io import BytesIO
from datetime import datetime, timezone
from app.api.export import export_to_excel
from app.models.search import SearchResponse, SearchResult


@pytest.mark.asyncio
async def test_export_to_excel_creates_valid_file():
    """
    Test, že export funkce vrací validní Excel soubor.
    """
    # Příprava testovacích dat
    mock_data = SearchResponse(
        query="test query",
        fetched_at=datetime.now(timezone.utc),
        provider="serpapi",
        total_returned=1,
        results=[
            SearchResult(
                position=1,
                title="Test Title",
                url="https://example.com",
                snippet="Test snippet"
            )
        ]
    )
    
    # Zavolání export funkce
    response = await export_to_excel(mock_data)
    
    # Ověření response hlaviček
    assert response.headers['content-type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    assert 'attachment; filename="search_results_' in response.headers['content-disposition']
    
    # Ověření, že obsah je validní Excel (zkusíme ho načíst zpět pomocí pandas)
    excel_content = BytesIO(response.body)
    df = pd.read_excel(excel_content)
    
    # Kontrola obsahu Excelu
    assert len(df) == 1
    assert df.iloc[0]['Titulek'] == "Test Title"
    assert df.iloc[0]['URL'] == "https://example.com"
