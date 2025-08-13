from fastapi import FastAPI
from app.routes import auth, contact_us, personal_details

app = FastAPI()

# ✅ Root endpoint so frontend won't get error
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

app.include_router(auth.router, tags=["Authentication"])
app.include_router(contact_us.router, prefix="/api/contact-us", tags=["contact_us"])
app.include_router(personal_details.router, prefix="/personal", tags=["personal_details"])
