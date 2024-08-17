from datetime import datetime, timedelta, timezone
from typing import Annotated

from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from pydantic import BaseModel

from .models import User

from .settings import SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class UserCreate(BaseModel):
    username: str
    password: str


class InvalidTokenError(Exception):
    pass


class HTTPCredentialsException(HTTPException):

    def __init__(self):
        super(self, status_code=status.HTTP_401_UNAUTHORIZED,
              detail='Could not validate credentials',
              headers={'WWW-Authenticate', 'Bearer'}
              )


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return 'complete'


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as jwt_error:
        raise InvalidTokenError from jwt_error


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPCredentialsException()
    except InvalidTokenError:
        raise HTTPCredentialsException()
    else:
        user = get_user_by_username(username)
        if user is None:
            raise HTTPCredentialsException()
        return user


def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
