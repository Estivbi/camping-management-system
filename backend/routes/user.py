from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserOut, UserLogin, Token
from models.user import create_user, get_user_by_username
from utils.auth import hash_password, verify_password, create_access_token, verify_token
from datetime import timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    password_hash = hash_password(user.password)
    try:
        new_user = create_user(user.username, user.email, password_hash)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    if not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user
