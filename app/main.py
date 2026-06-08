from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes.generate import router as generate_router
from app.routes.generate_excel import router as excel_router
from app.routes.upload_excel import router as upload_router
from app.routes.zephyr_upload import router as zephyr_router

app = FastAPI()

app.include_router(generate_router)
app.include_router(excel_router)
app.include_router(upload_router)
app.include_router(zephyr_router)

templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )