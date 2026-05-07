from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import BackgroundTasks
from fastapi import Request

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db

from app.models_user import User

from app.schemas_user import UserCreate

from app.auth import get_password_hash
from app.auth import verify_password
from app.auth import create_access_token

from app.email_service import send_verification_email
from app.email_service import create_email_token
from app.email_service import confirm_email_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=201)
async def register(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == body.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    hashed_password = get_password_hash(
        body.password
    )

    new_user = User(
        email=body.email,
        username=body.username,
        hashed_password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    token = create_email_token(
        new_user.email
    )

    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        str(request.base_url),
        token
    )

    return new_user

@router.get("/verify/{token}")
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):

    email = confirm_email_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Verification error"
        )

    user.verified = True

    db.commit()

    return {
        "message": "Email verified"
    }

@router.post("/login")
def login(
    body: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == body.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        body.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    if not user.verified:
        raise HTTPException(
            status_code=401,
            detail="Email not verified"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }