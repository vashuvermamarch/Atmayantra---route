from fastapi import APIRouter, Form, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import Optional
from app.database import SessionLocal
from app import models, schemas

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.APIResponse)
def create_contact(
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone_no: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if existing:
        return {"success": False, "message": "Contact with this phone number already exists", "data": None}

    contact = models.Contact(name=name, email=email, phone_no=phone_no, message=message)
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {
        "success": True,
        "message": "Contact created successfully",
        "data": schemas.ContactResponse.model_validate(contact)
    }


@router.get("/", response_model=schemas.APIResponse)
def get_all_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return {
        "success": True,
        "message": "Contacts fetched successfully",
        "data": [schemas.ContactResponse.model_validate(c) for c in contacts]
    }


@router.get("/{phone_no}", response_model=schemas.APIResponse)
def get_contact(phone_no: str, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        return {"success": False, "message": "Contact not found", "data": None}
    return {
        "success": True,
        "message": "Contact fetched successfully",
        "data": schemas.ContactResponse.model_validate(contact)
    }


@router.put("/{phone_no}", response_model=schemas.APIResponse)
def update_contact(
    phone_no: str,
    name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        return {"success": False, "message": "Contact not found", "data": None}

    contact.name = name
    contact.email = email
    contact.message = message
    db.commit()
    db.refresh(contact)

    return {
        "success": True,
        "message": "Contact updated successfully",
        "data": schemas.ContactResponse.model_validate(contact)
    }


@router.patch("/{phone_no}", response_model=schemas.APIResponse)
def patch_contact(
    phone_no: str,
    name: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    message: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        return {"success": False, "message": "Contact not found", "data": None}

    if name:
        contact.name = name
    if email:
        contact.email = email
    if message:
        contact.message = message

    db.commit()
    db.refresh(contact)

    return {
        "success": True,
        "message": "Contact patched successfully",
        "data": schemas.ContactResponse.model_validate(contact)
    }


@router.delete("/{phone_no}", response_model=schemas.APIResponse)
def delete_contact(phone_no: str, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.phone_no == phone_no).first()
    if not contact:
        return {"success": False, "message": "Contact not found", "data": None}

    db.delete(contact)
    db.commit()
    return {"success": True, "message": "Contact deleted successfully", "data": None}
