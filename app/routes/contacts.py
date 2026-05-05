from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import app.crud as crud
from app.schemas import ContactCreate, ContactResponse
from app.auth import get_db, get_current_user
from app.models_user import User

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=201)
def create(contact: ContactCreate,
           db: Session = Depends(get_db),
           user: User = Depends(get_current_user)):
    return crud.create_contact(db, contact, user.id)


@router.get("/", response_model=list[ContactResponse])
def all(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return crud.get_contacts(db, user.id, first_name, last_name, email)


@router.get("/birthdays/upcoming", response_model=list[ContactResponse])
def birthdays(db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    return crud.get_upcoming_birthdays(db, user.id)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_one(contact_id: int,
            db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    contact = crud.get_contact_by_id(db, contact_id, user.id)
    if not contact:
        raise HTTPException(status_code=404)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update(contact_id: int,
           data: ContactCreate,
           db: Session = Depends(get_db),
           user: User = Depends(get_current_user)):
    contact = crud.update_contact(db, contact_id, data, user.id)
    if not contact:
        raise HTTPException(status_code=404)
    return contact


@router.delete("/{contact_id}")
def delete(contact_id: int,
           db: Session = Depends(get_db),
           user: User = Depends(get_current_user)):
    contact = crud.delete_contact(db, contact_id, user.id)
    if not contact:
        raise HTTPException(status_code=404)
    return {"message": "deleted"}