from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

SECURITY_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now().astimezone() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exceptions
    return token_data


def get_current_user(
    token: str = Depends(oauth2scheme), db: Session = Depends(database.get_db)
):
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credential_exceptions)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
