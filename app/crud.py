from sqlalchemy.orm import Session
from app.models import Contact
from datetime import date, timedelta


def create_contact(db: Session, contact, user_id):
    obj = Contact(**contact.model_dump(), user_id=user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_contacts(db, user_id, first_name=None, last_name=None, email=None):
    query = db.query(Contact).filter(Contact.user_id == user_id)

    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))

    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    return query.all()


def get_contact_by_id(db, contact_id, user_id):
    return db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()


def update_contact(db, contact_id, data, user_id):
    contact = get_contact_by_id(
        db,
        contact_id,
        user_id
    )
    if not contact:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)

    return contact



from datetime import date, timedelta


from datetime import date, timedelta, datetime


def get_upcoming_birthdays(db, user_id):
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        Contact.user_id == user_id
    ).all()

    result = []

    for c in contacts:

        bd = datetime.strptime(
            c.birthday,
            "%Y-%m-%d"
        ).date()

        bd = bd.replace(year=today.year)

        if bd < today:
            bd = bd.replace(year=today.year + 1)

        if today <= bd <= next_week:
            result.append(c)

    return result

def delete_contact(db, contact_id, user_id):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == user_id
    ).first()

    if contact:
        db.delete(contact)
        db.commit()

    return contact
