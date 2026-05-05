from pydantic import BaseModel

class UserRegister(BaseModel):
    fullname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ContactMessage(BaseModel):
    name: str
    email: str
    feedback: str

class CourseEnrollment(BaseModel):
    email: str
    course_id: str
    course_title: str

