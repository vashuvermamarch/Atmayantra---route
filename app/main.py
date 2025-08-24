# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, contact_us, personal_details

app = FastAPI()

# ✅ CORS setup (for local dev + future frontend)
origins = [
    "http://localhost",
    "http://localhost:5173",  # your React dev server (if you use React locally)
    # later, add your deployed frontend URL here (e.g. "https://myapp.netlify.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # restrict to known origins (good practice)
    allow_credentials=True,
    allow_methods=["*"],          # allow all methods
    allow_headers=["*"],          # allow all headers
)

# ✅ Root endpoint for quick check
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

# ✅ Routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(contact_us.router, prefix="/api/contact-us", tags=["Contact Us"])
app.include_router(personal_details.router, prefix="/personal", tags=["Personal Details"])
