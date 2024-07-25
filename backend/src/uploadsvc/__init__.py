from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from werkzeug.utils import secure_filename

from .config import Settings
from .util import save_upload_file


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount("/static", StaticFiles(directory="uploadsvc/static"), name="static")


@lru_cache
def get_settings():
    return Settings()


@app.post('/push')
async def upload_file(
    file: list[UploadFile],
    settings: Annotated[Settings, Depends(get_settings)]
):
    for f in file:
        dest_path = settings.upload_dir / secure_filename(f.filename)
        save_upload_file(f, dest_path)

    return 'ok'


@app.get('/files/{filename}')
async def file_get(filename: str, settings: Annotated[Settings, Depends(get_settings)]):
    return FileResponse(settings.upload_dir / secure_filename(filename))


@app.get('/files/')
async def file_list(request: Request, settings: Annotated[Settings, Depends(get_settings)]):
    file_lst = settings.upload_dir.iterdir()

    return {
        'file_list': [f.name for f in file_lst],
    }
