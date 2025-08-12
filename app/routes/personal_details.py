from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os

router = APIRouter()

# In-memory store
user_data = {}

# Create folder for profile photos
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
    profile_photo: UploadFile = File(...)
):
    if contact_number in user_data:
        raise HTTPException(status_code=400, detail="User already exists.")

    gender = validate_gender(gender)

    contents = await profile_photo.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Profile photo must be <= 5MB")

    photo_filename = f"{contact_number}_{profile_photo.filename}"
    photo_path = os.path.join(PHOTO_DIR, photo_filename)
    with open(photo_path, "wb") as f:
        f.write(contents)

    user_data[contact_number] = {
        "full_name": full_name,
        "dob": f"{dob_day:02d}-{dob_month:02d}-{dob_year}",
        "age": age,
        "gender": gender,
        "email": email,
        "address": address,
        "profile_photo_path": photo_path
    }

    return {"message": "User created successfully."}

@router.get("/get-all/")
def get_all_users():
    return user_data

@router.get("/get/{contact_number}")
def get_user(contact_number: str):
    if contact_number not in user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data[contact_number]

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
    profile_photo: UploadFile = File(...)
):
    if contact_number not in user_data:
        raise HTTPException(status_code=404, detail="User not found")

    gender = validate_gender(gender)

    contents = await profile_photo.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Profile photo must be <= 5MB")

    old_photo_path = user_data[contact_number]["profile_photo_path"]
    if os.path.exists(old_photo_path):
        os.remove(old_photo_path)

    photo_filename = f"{contact_number}_{profile_photo.filename}"
    photo_path = os.path.join(PHOTO_DIR, photo_filename)
    with open(photo_path, "wb") as f:
        f.write(contents)

    user_data[contact_number] = {
        "full_name": full_name,
        "dob": f"{dob_day:02d}-{dob_month:02d}-{dob_year}",
        "age": age,
        "gender": gender,
        "email": email,
        "address": address,
        "profile_photo_path": photo_path
    }

    return {"message": "User updated successfully."}

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
    profile_photo: Optional[UploadFile] = File(None)
):
    if contact_number not in user_data:
        raise HTTPException(status_code=404, detail="User not found")

    user = user_data[contact_number]

    if full_name:
        user["full_name"] = full_name
    if dob_day and dob_month and dob_year:
        user["dob"] = f"{dob_day:02d}-{dob_month:02d}-{dob_year}"
    if age:
        user["age"] = age
    if gender:
        allowed_genders = {"male", "female", "other"}
        if gender.lower() not in allowed_genders:
            raise HTTPException(status_code=400, detail="Gender must be Male, Female, or Other")
        user["gender"] = gender.capitalize()
    if email:
        user["email"] = email
    if address:
        user["address"] = address

    if profile_photo:
        contents = await profile_photo.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Profile photo must be <= 5MB")

        old_photo_path = user["profile_photo_path"]
        if os.path.exists(old_photo_path):
            os.remove(old_photo_path)

        photo_filename = f"{contact_number}_{profile_photo.filename}"
        photo_path = os.path.join(PHOTO_DIR, photo_filename)
        with open(photo_path, "wb") as f:
            f.write(contents)
        user["profile_photo_path"] = photo_path

    return {"message": "User partially updated successfully."}

@router.delete("/delete/{contact_number}")
def delete_user(contact_number: str):
    if contact_number not in user_data:
        raise HTTPException(status_code=404, detail="User not found")

    photo_path = user_data[contact_number]["profile_photo_path"]
    if os.path.exists(photo_path):
        os.remove(photo_path)

    del user_data[contact_number]
    return {"message": "User deleted successfully."}
