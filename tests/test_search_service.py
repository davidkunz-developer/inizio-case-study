"""
Unit testy pro SearchService.
"""

import pytest
from datetime import datetime, timezone
from app.services.search_service import SearchService
from app.models.search import SearchResponse, SearchResult


@pytest.fixture
def search_service():
    """
    Fixture pro vytvoření instance SearchService.
    Vynutíme použití mock dat, aby testy nevolaly skutečné API.
    """
    service = SearchService()
    service.use_real_api = False  # Vypnutí reálného API pro účely testování
    return service


def test_search_returns_search_response(search_service):
    """
    Test, že metoda search() vrací SearchResponse.
    """
    search_query = "python tutorial"
    
    result = search_service.search(search_query)
    
    assert isinstance(result, SearchResponse)
    assert result.query == search_query
    assert result.provider == "mock"


def test_search_response_has_correct_structure(search_service):
    """
    Test, že SearchResponse má správnou strukturu.
    """
    search_query = "fastapi"
    
    result = search_service.search(search_query)
    
    assert hasattr(result, 'query')
    assert hasattr(result, 'fetched_at')
    assert hasattr(result, 'provider')
    assert hasattr(result, 'total_returned')
    assert hasattr(result, 'results')
    
    assert isinstance(result.fetched_at, datetime)
    assert isinstance(result.total_returned, int)
    assert isinstance(result.results, list)


def test_search_results_are_search_result_instances(search_service):
    """
    Test, že výsledky jsou instance SearchResult.
    """
    search_query = "python"
    
    result = search_service.search(search_query)
    
    for search_result in result.results:
        assert isinstance(search_result, SearchResult)
        assert hasattr(search_result, 'position')
        assert hasattr(search_result, 'title')
        assert hasattr(search_result, 'url')
        assert hasattr(search_result, 'snippet')


def test_search_result_positions_are_sequential(search_service):
    """
    Test, že pozice výsledků jsou sekvenční (1, 2, 3, ...).
    """
    search_query = "test"
    
    result = search_service.search(search_query)
    
    for i, search_result in enumerate(result.results, start=1):
        assert search_result.position == i


def test_total_returned_matches_results_length(search_service):
    """
    Test, že total_returned odpovídá počtu výsledků.
    """
    search_query = "example"
    
    result = search_service.search(search_query)
    
    assert result.total_returned == len(result.results)


def test_fetched_at_is_utc(search_service):
    """
    Test, že fetched_at je v UTC timezone.
    """
    search_query = "test"
    
    result = search_service.search(search_query)
    
    assert result.fetched_at.tzinfo == timezone.utc


def test_parse_organic_results_with_empty_items(search_service):
    """
    Test parsování prázdného seznamu výsledků.
    """
    raw_json = {"organic_results": []}
    
    results = search_service._parse_organic_results(raw_json)
    
    assert results == []


def test_parse_organic_results_with_missing_key(search_service):
    """
    Test parsování když chybí klíč 'organic_results'.
    """
    raw_json = {}
    
    results = search_service._parse_organic_results(raw_json)
    
    assert results == []


def test_parse_organic_results_with_valid_data(search_service):
    """
    Test parsování validních dat.
    """
    raw_json = {
        "organic_results": [
            {
                "title": "Test Title 1",
                "link": "https://example.com/1",
                "snippet": "Test snippet 1"
            },
            {
                "title": "Test Title 2",
                "link": "https://example.com/2",
                "snippet": "Test snippet 2"
            }
        ]
    }
    
    results = search_service._parse_organic_results(raw_json)
    
    assert len(results) == 2
    assert results[0].position == 1
    assert results[0].title == "Test Title 1"
    assert results[0].url == "https://example.com/1"
    assert results[0].snippet == "Test snippet 1"
    
    assert results[1].position == 2
    assert results[1].title == "Test Title 2"


def test_parse_organic_results_with_missing_snippet(search_service):
    """
    Test parsování když chybí snippet (je optional).
    """
    raw_json = {
        "organic_results": [
            {
                "title": "Test Title",
                "link": "https://example.com"
            }
        ]
    }
    
    results = search_service._parse_organic_results(raw_json)
    
    assert len(results) == 1
    assert results[0].snippet is None


from unittest.mock import patch
import httpx

def test_search_fallback_on_api_error(search_service):
    """
    Test, že při chybě API (např. timeout) se aktivuje fallback na mock data.
    """
    # Nasimulujeme situaci, kdy je API aktivní, ale vyhodí chybu
    search_service.use_real_api = True
    
    # Pomocí 'patch' vynutíme, aby _call_serpapi vyhodila TimeoutException
    with patch.object(search_service, '_call_serpapi', side_effect=httpx.TimeoutException("Timeout!")):
        result = search_service.search("test query")
        
        # Ověříme, že i přes chybu máme výsledky (z mocku)
        assert result.provider == "serpapi-fallback"
        assert len(result.results) > 0
        assert "Vyhledávací služba neodpověděla včas" in result.warning
        assert search_service.fallback_mode is True
