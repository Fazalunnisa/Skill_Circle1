import os
import sys

# Add the project root to sys.path so we can import from the 'fastapi' folder
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "fastapi"))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.database import client
from models import UserRegister, UserLogin, ContactMessage, CourseEnrollment
from pymongo.errors import ServerSelectionTimeoutError
import bcrypt

app = FastAPI(title="SkillCircle API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use database from the MongoDB client
db = client.get_database("skillcircle")
users_collection = db["users"]
contacts_collection = db["contacts"]
enrollments_collection = db["enrollments"]

# In-memory fallback if MongoDB Atlas is blocking the IP
fallback_users = []
fallback_contacts = []
fallback_enrollments = []

@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    try:
        # Attempt MongoDB
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user_dict = user.model_dump()
        # Hash the password for security
        hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user_dict["password"] = hashed.decode('utf-8')
        
        users_collection.insert_one(user_dict)
        return {"message": "User registered successfully"}
    except ServerSelectionTimeoutError:
        print("MongoDB timed out. Using local memory fallback for registration.")
        if any(u["email"] == user.email for u in fallback_users):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user_dict = user.model_dump()
        hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user_dict["password"] = hashed.decode('utf-8')
        
        fallback_users.append(user_dict)
        return {"message": "User registered successfully (Local Mode)"}

@app.post("/api/login")
def login_user(user: UserLogin):
    try:
        # Attempt MongoDB
        existing_user = users_collection.find_one({"email": user.email})
        
        if not existing_user or not bcrypt.checkpw(user.password.encode('utf-8'), existing_user["password"].encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        return {"message": "Login successful", "user": {"email": existing_user["email"], "fullname": existing_user["fullname"]}}
    except ServerSelectionTimeoutError:
        print("MongoDB timed out. Using local memory fallback for login.")
        existing_fallback = next((u for u in fallback_users if u["email"] == user.email), None)
        
        if not existing_fallback or not bcrypt.checkpw(user.password.encode('utf-8'), existing_fallback["password"].encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        return {"message": "Login successful (Local Mode)", "user": {"email": existing_fallback["email"], "fullname": existing_fallback["fullname"]}}

@app.post("/api/reset-password")
def reset_password(data: dict):
    email = data.get("email")
    new_password = data.get("new_password")
    
    if not email or not new_password:
        raise HTTPException(status_code=400, detail="Incomplete data provided")
        
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        # Update MongoDB
        result = users_collection.update_one({"email": email}, {"$set": {"password": hashed}})
        if result.matched_count > 0:
            return {"message": "Password updated successfully in database"}
    except ServerSelectionTimeoutError:
        # Update Fallback
        user = next((u for u in fallback_users if u["email"] == email), None)
        if user:
            user["password"] = hashed
            return {"message": "Password updated successfully (Local Mode)"}
            
    raise HTTPException(status_code=404, detail="Email not found")

@app.post("/api/contact", status_code=status.HTTP_201_CREATED)
def submit_contact(contact: ContactMessage):
    try:
        contact_dict = contact.model_dump()
        contacts_collection.insert_one(contact_dict)
        return {"message": "Feedback submitted successfully"}
    except ServerSelectionTimeoutError:
        fallback_contacts.append(contact.model_dump())
        return {"message": "Feedback submitted successfully (Local Mode)"}

@app.post("/api/enroll", status_code=status.HTTP_201_CREATED)
def enroll_course(enrollment: CourseEnrollment):
    try:
        existing = enrollments_collection.find_one({"email": enrollment.email, "course_id": enrollment.course_id})
        if existing:
            raise HTTPException(status_code=400, detail="Already enrolled in this course")
        enrollments_collection.insert_one(enrollment.model_dump())
        return {"message": "Successfully enrolled"}
    except ServerSelectionTimeoutError:
        if any(e["email"] == enrollment.email and e["course_id"] == enrollment.course_id for e in fallback_enrollments):
            raise HTTPException(status_code=400, detail="Already enrolled in this course")
        fallback_enrollments.append(enrollment.model_dump())
        return {"message": "Successfully enrolled (Local Mode)"}

@app.get("/api/my_courses/{email}")
def get_my_courses(email: str):
    try:
        courses = list(enrollments_collection.find({"email": email}, {"_id": 0}))
        return {"courses": courses}
    except ServerSelectionTimeoutError:
        courses = [e for e in fallback_enrollments if e["email"] == email]
        return {"courses": courses}

@app.get("/api/stats")
def get_stats():
    try:
        active_students = users_collection.count_documents({})
        certificates_issued = enrollments_collection.count_documents({})
        return {
            "active_students": active_students,
            "total_courses": 16, # Fixed catalog size
            "certificates_issued": certificates_issued,
            "success_rate": 95
        }
    except ServerSelectionTimeoutError:
        return {
            "active_students": len(fallback_users),
            "total_courses": 16,
            "certificates_issued": len(fallback_enrollments),
            "success_rate": 95
        }

@app.get("/api/admin/contacts")
def get_all_contacts():
    try:
        data = list(contacts_collection.find({}, {"_id": 0}))
        return {"contacts": data}
    except ServerSelectionTimeoutError:
        return {"contacts": fallback_contacts}

@app.get("/api/admin/users")
def get_all_users():
    try:
        data = list(users_collection.find({}, {"_id": 0, "password": 0}))
        return {"users": data}
    except ServerSelectionTimeoutError:
        return {"users": [{"fullname": u["fullname"], "email": u["email"]} for u in fallback_users]}

from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/welcome.html")

# Mount frontend at root natively
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
