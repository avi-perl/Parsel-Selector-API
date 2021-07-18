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


@router.get("/examples/html", response_class=HTMLResponse, tags=["Example Documents"])
async def return_html_example():
    """
    # HTML Example

    Returns a basic HTML document that may be used for testing.

    ### Example Paths
    - **XPATH:** `/html/body/div/span[3]/text()`
    - **CSS:** `body > div > span:nth-child(5) > strong`
    - **REGEX:** `You.*🤕`
    """
    return HTMLResponse(content=DocumentExamples.HTML)


@router.get("/examples/json", response_class=ORJSONResponse, tags=["Example Documents"])
async def return_html_example():
    """
    # JSON Example

    Returns a basic JSON document that may be used for testing.

    ### Example Paths
    - **JSON:** `/note/subject`
    """
    return DocumentExamples.JSON


@router.get("/examples/xml", response_class=HTMLResponse, tags=["Example Documents"])
async def return_html_example():
    """
    # XML Example

    Returns a basic XML document that may be used for testing.

    ### Example Paths
    - **XML:** `/note/subject`
    """
    return Response(content=DocumentExamples.XML, media_type="application/xml")
