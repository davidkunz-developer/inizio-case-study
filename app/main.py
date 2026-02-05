from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import subprocess

from app.api.search import router as search_router
from app.api.export import router as export_router

app = FastAPI(
    title="Google Search API",
    description="FastAPI aplikace pro vyhledávání přes Google Programmable Search Engine API",
    version="0.1.0"
)

app.include_router(search_router, prefix="/api", tags=["search"])
app.include_router(export_router, prefix="/api", tags=["export"])

static_dir = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def root():
    return FileResponse(static_dir / "index.html")


@app.get("/test-report")
async def test_report():
    report_path = static_dir / "report.html"

    subprocess.run(
        ["pytest", "tests/", f"--html={report_path}", "--self-contained-html"], 
        check=False
    )
    
    return FileResponse(report_path)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
