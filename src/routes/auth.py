from fastapi import APIRouter, HTTPException, Depends
from src.models.user_models import UserCreate, Token
from src.services.user_service import create_user, authenticate_user, get_user_by_id
from src.utils.security import create_access_token
from src.models.user_models import TokenData
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/signup", response_model=dict)
def signup(user_in: UserCreate):
    created = create_user(user_in.email, user_in.password, user_in.name)
    if not created:
        raise HTTPException(status_code=400, detail="User already exists with this email")
    return {"status": "success", "data": created}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(user["id"])})
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import Security
from jose import JWTError 
from src.utils.security import decode_access_token
from src.models.user_models import TokenData

def get_current_user(token: str = Depends(oauth2_scheme)):
    try: 
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name"),
    }