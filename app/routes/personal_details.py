from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
import os
from datetime import date
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

PHOTO_DIR = "profile_photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

def validate_gender(gender: str):
    allowed_genders = {"male", "female", "other"}
    if gender.lower() not in allowed_genders:
        raise HTTPException(status_code=400, detail="Gender must be Male, Female, or Other")
    return gender.capitalize()

@router.post("/submit-details/")
async def create_user(
    contact_number: str = Form(...),
    full_name: str = Form(...),
    dob_day: int = Form(...),
    dob_month: int = Form(...),
    dob_year: int = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing = db.query(models.PersonalDetail).filter(models.PersonalDetail.phone_no == contact_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists.")

    gender = validate_gender(gender)

    try:
        dob = date(dob_year, dob_month, dob_day)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date of birth.")

    contents = await profile_photo.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Profile photo must be <= 5MB")

    photo_filename = f"{contact_number}_{profile_photo.filename}"
    photo_path = os.path.join(PHOTO_DIR, photo_filename)
    with open(photo_path, "wb") as f:
        f.write(contents)

    new_user = models.PersonalDetail(
        phone_no=contact_number,
        full_name=full_name,
        dob=dob,
        age=age,
        gender=gender,
        email=email,
        address=address,
        photo_path=photo_path
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully.", "user": new_user}

@router.get("/get-all/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.PersonalDetail).all()

@router.get("/get/{contact_number}")
def get_user(contact_number: str, db: Session = Depends(get_db)):
    user = db.query(models.PersonalDetail).filter(models.PersonalDetail.phone_no == contact_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/update/{contact_number}")
async def update_user(
    contact_number: str,
    full_name: str = Form(...),
    dob_day: int = Form(...),
    dob_month: int = Form(...),
    dob_year: int = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.PersonalDetail).filter(models.PersonalDetail.phone_no == contact_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    gender = validate_gender(gender)

    try:
        dob = date(dob_year, dob_month, dob_day)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date of birth.")

    contents = await profile_photo.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Profile photo must be <= 5MB")

    if user.photo_path and os.path.exists(user.photo_path):
        os.remove(user.photo_path)

    photo_filename = f"{contact_number}_{profile_photo.filename}"
    photo_path = os.path.join(PHOTO_DIR, photo_filename)
    with open(photo_path, "wb") as f:
        f.write(contents)

    user.full_name = full_name
    user.dob = dob
    user.age = age
    user.gender = gender
    user.email = email
    user.address = address
    user.photo_path = photo_path

    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully.", "user": user}

@router.patch("/patch/{contact_number}")
async def patch_user(
    contact_number: str,
    full_name: Optional[str] = Form(None),
    dob_day: Optional[int] = Form(None),
    dob_month: Optional[int] = Form(None),
    dob_year: Optional[int] = Form(None),
    age: Optional[int] = Form(None),
    gender: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    profile_photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(models.PersonalDetail).filter(models.PersonalDetail.phone_no == contact_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if full_name:
        user.full_name = full_name
    if dob_day and dob_month and dob_year:
        try:
            user.dob = date(dob_year, dob_month, dob_day)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date of birth.")
    if age is not None:
        user.age = age
    if gender:
        user.gender = validate_gender(gender)
    if email:
        user.email = email
    if address:
        user.address = address

    if profile_photo:
        contents = await profile_photo.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Profile photo must be <= 5MB")

        if user.photo_path and os.path.exists(user.photo_path):
            os.remove(user.photo_path)

        photo_filename = f"{contact_number}_{profile_photo.filename}"
        photo_path = os.path.join(PHOTO_DIR, photo_filename)
        with open(photo_path, "wb") as f:
            f.write(contents)
        user.photo_path = photo_path

    db.commit()
    db.refresh(user)

    return {"message": "User partially updated successfully.", "user": user}

@router.delete("/delete/{contact_number}")
def delete_user(contact_number: str, db: Session = Depends(get_db)):
    user = db.query(models.PersonalDetail).filter(models.PersonalDetail.phone_no == contact_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.photo_path and os.path.exists(user.photo_path):
        os.remove(user.photo_path)

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully."}
