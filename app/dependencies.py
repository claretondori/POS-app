from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends (oauth2_scheme), db: Session = Depends(get_db)):
    user = auth_service.get_user_from_token(db,token)
    return user