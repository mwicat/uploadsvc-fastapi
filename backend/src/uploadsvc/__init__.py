from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from werkzeug.utils import secure_filename

from .config import Settings
from .util import save_upload_file


app = FastAPI()
app.mount("/static", StaticFiles(directory="uploadsvc/static"), name="static")

templates = Jinja2Templates(directory="uploadsvc/templates")


@lru_cache
def get_settings():
    return Settings()


@app.get('/push')
async def upload_file(request: Request):
    return templates.TemplateResponse("upload.html", {
        "request": request,
    })


@app.post('/push')
async def upload_file(
    file: list[UploadFile],
    settings: Annotated[Settings, Depends(get_settings)]):
    
    for f in file:
        dest_path = settings.upload_dir / secure_filename(f.filename)
        save_upload_file(f, dest_path)

    return 'ok'


@app.get('/files/{filename}')
async def file_get(filename: str, settings: Annotated[Settings, Depends(get_settings)]):
    return FileResponse(settings.upload_dir / secure_filename(filename))


@app.get('/files/')
async def file_list(request: Request, settings: Annotated[Settings, Depends(get_settings)]):
    file_list = settings.upload_dir.iterdir()
    return templates.TemplateResponse("list_files.html", {
        "request": request,
        "file_list": file_list,
        })
