from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response, ORJSONResponse

router = APIRouter()


class DocumentExamples:
    """Example data for example pages"""

    TO = "Guest"
    FROM = "Avi Perl"
    SUBJECT = "You scraped me 🤕"
    BODY = "Thats painful, ouch!"

    HTML = f'<html><head><title>HTML Example Note</title></head><body><div class="note"><span><strong>To:</strong> {TO}</span><br><span><strong>From:</strong> {FROM}</span><br><span><strong>Subject:</strong> {SUBJECT}</span><hr><p>{BODY}</p></div></body></html>'
    JSON = {
        "note": {
            "to": TO,
            "from": FROM,
            "subject": SUBJECT,
            "body": BODY,
        }
    }
    XML = f'<?xml version="1.0" encoding="UTF-8"?><note><to>{TO}</to><from>{FROM}</from><subject>{SUBJECT}</subject><body>{BODY}</body></note>'


@router.get("/examples/html", response_class=HTMLResponse)
async def return_html_example():
    """Returns a basic HTML response for testing."""
    return HTMLResponse(content=DocumentExamples.HTML)


@router.get("/examples/json", response_class=ORJSONResponse)
async def return_html_example():
    """Returns a basic JSON response for testing."""
    return DocumentExamples.JSON


@router.get("/examples/xml", response_class=HTMLResponse)
async def return_html_example():
    """Returns a basic JSON response for testing."""
    return Response(content=DocumentExamples.XML, media_type="application/xml")
