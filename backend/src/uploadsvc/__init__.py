from functools import lru_cache
from typing import Annotated
from datetime import timedelta

from fastapi import (
    Depends,
    FastAPI,
    Request,
    UploadFile,
    status,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from werkzeug.utils import secure_filename


from .config import Settings
from .database import SessionLocal
from .util import save_upload_file
from .auth import (
    authenticate_user,
    create_user,
    create_access_token,
    verify_token,
    UserCreate,
    InvalidTokenError,
)
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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


@app.post('/register')
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@app.post('/token')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/verify-token/{token}')
async def verify_user_token(token: str):
    try:
        verify_token(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail='Token is invalid or expired')
    else:
        return {'message': 'token is valid'}
