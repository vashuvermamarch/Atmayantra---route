from fastapi import FastAPI
from app.routes import auth
from app.routes import contact_us
from app.routes import personal_details  # ✅ import your personal_details routes

app = FastAPI()

app.include_router(auth.router, tags=["Authentication"])
app.include_router(contact_us.router, prefix="/api/contact-us", tags=["contact_us"])
app.include_router(personal_details.router, prefix="/personal", tags=["personal_details"])