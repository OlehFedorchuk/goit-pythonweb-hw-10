from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
import cloudinary.uploader
from app.database import get_db
from app.models_user import User
from app.auth_bearer import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

limiter = Limiter(
    key_func=get_remote_address
)

@router.get("/me")
@limiter.limit("5/minute")
def me(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.patch("/avatar")
async def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = cloudinary.uploader.upload(
        file.file,
        public_id=current_user.username,
        overwrite=True
    )

    current_user.avatar = result["secure_url"]

    db.commit()

    db.refresh(current_user)

    return {
        "avatar": current_user.avatar
    }