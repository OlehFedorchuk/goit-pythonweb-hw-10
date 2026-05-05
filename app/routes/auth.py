from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import hash_password, verify_password, create_access_token, get_db, get_current_user
from app.models_user import User
from app.schemas_user import UserCreate, UserLogin, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="User exists")
    print("RAW PASSWORD:", user.password)
    print("TYPE:", type(user.password))
    print("LEN:", len(str(user.password)))
    new_user = User(email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user