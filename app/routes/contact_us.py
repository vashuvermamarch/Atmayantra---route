from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import Optional
from app.database import SessionLocal
from app import models

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_contact(
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone_no: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Contact with this phone number already exists")

    contact = models.Contact(name=name, email=email, phone_no=phone_no, message=message)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get("/")
def get_all_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()


@router.get("/{phone_no}")
def get_contact(phone_no: str, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{phone_no}")
def update_contact(
    phone_no: str,
    name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact.name = name
    contact.email = email
    contact.message = message
    db.commit()
    return contact


@router.patch("/{phone_no}")
def patch_contact(
    phone_no: str,
    name: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    message: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    if name:
        contact.name = name
    if email:
        contact.email = email
    if message:
        contact.message = message

    db.commit()
    return contact


@router.delete("/{phone_no}")
def delete_contact(phone_no: str, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}
