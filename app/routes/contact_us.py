from fastapi import APIRouter, Form, HTTPException
from pydantic import EmailStr
from typing import Optional

router = APIRouter()

# In-memory storage
contacts_db = {}
contact_id_counter = 1


@router.post("/")
def create_contact(
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone_no: str = Form(...),
    message: str = Form(...)
):
    global contact_id_counter

    if phone_no in contacts_db:
        raise HTTPException(status_code=400, detail="Contact with this phone number already exists")

    contact = {
        "contact_id": contact_id_counter,
        "name": name,
        "email": email,
        "phone_no": phone_no,
        "message": message
    }
    contacts_db[phone_no] = contact
    contact_id_counter += 1
    return contact


@router.get("/")
def get_all_contacts():
    return list(contacts_db.values())


@router.get("/{phone_no}")
def get_contact(phone_no: str):
    contact = contacts_db.get(phone_no)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{phone_no}")
def update_contact(
    phone_no: str,
    name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...)
):
    contact = contacts_db.get(phone_no)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact.update({
        "name": name,
        "email": email,
        "message": message
    })
    return contact


@router.patch("/{phone_no}")
def patch_contact(
    phone_no: str,
    name: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    message: Optional[str] = Form(None)
):
    contact = contacts_db.get(phone_no)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    if name:
        contact["name"] = name
    if email:
        contact["email"] = email
    if message:
        contact["message"] = message

    return contact


@router.delete("/{phone_no}")
def delete_contact(phone_no: str):
    if phone_no not in contacts_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    del contacts_db[phone_no]
    return {"message": "Contact deleted successfully"}
