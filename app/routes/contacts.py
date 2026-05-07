from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Contact
from app.models_user import User
from app.schemas import ContactSchema
from app.auth_bearer import get_current_user
import app.crud as crud
from app.schemas import ContactCreate, ContactResponse
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

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = crud.get_contact_by_id(db, contact_id, current_user.id)

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = crud.update_contact(
        db,
        contact_id,
        contact_data,
        current_user.id
    )
    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return contact

@router.get("/birthdays/upcoming", response_model=list[ContactResponse])
def upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_upcoming_birthdays(
        db,
        current_user.id
    )


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = crud.delete_contact(
        db,
        contact_id,
        current_user.id
    )
    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )
    return {"message": "Contact deleted successfully"}