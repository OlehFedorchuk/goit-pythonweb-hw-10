from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import Contact
from app.models_user import User

from app.schemas import ContactSchema

from app.auth_bearer import get_current_user

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)

@router.post("/", status_code=201)
def create_contact(
    body: ContactSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    contact = Contact(
        **body.dict(),
        user_id=current_user.id
    )

    db.add(contact)

    db.commit()

    db.refresh(contact)

    return contact

@router.get("/")
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    contacts = db.query(Contact).filter(
        Contact.user_id == current_user.id
    ).all()

    return contacts