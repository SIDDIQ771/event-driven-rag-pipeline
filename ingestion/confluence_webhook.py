from fastapi import APIRouter, Request
from ingestion.confluence_ingest import process_single_confluence_page

router = APIRouter()

@router.post("/confluence/webhook")
async def confluence_webhook(request: Request):
    data = await request.json()
    page_id = data["page"]["id"]
    print(f"[Webhook] Confluence updated: {page_id}")
    process_single_confluence_page(page_id)
    return {"status": "ok"}
