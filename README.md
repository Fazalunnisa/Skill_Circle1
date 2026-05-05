<<<<<<< HEAD
# 🎓 Skill Circle - Immersive E-Learning Platform

A state-of-the-art, full-stack e-learning portal designed for high-fidelity interactive education.

## 🚀 Live Demo
**Production URL:** [Your-Vercel-Link-Here]

## 🛠️ Technology Architecture
- **Backend**: FastAPI (Python) - High performance asynchronous processing.
- **Frontend**: Vanilla JavaScript / HTML5 / CSS3 - Glassmorphic UI with CSS custom properties.
- **Database**: MongoDB Atlas - Cloud-native NoSQL data persistence.
- **Security**: 
  - `bcrypt` one-way password hashing.
  - Secure Environment Variable management for cloud secrets.
- **UX/Animations**: 
  - GSAP & CSS Keyframes for smooth vertical lift and glassmorphism.
  - Custom Toast Notification system (replacing native alerts).
  - Real-time progress tracking with localStorage synchronization.

## ✨ Premium Features
- **Intelligent Dashboard**: Real-time progress bars tracking resource interaction.
- **Admin Monitor**: High-level data analytics dashboard for database health and user stats.
- **Interactive Course Hub**: Dynamic 3D resource cards for videos, docs, and sandboxes.
- **Smart Security**: Professional "Forgot Password" flow with verified database updates.
- **Mobile Responsive**: Custom media query breakpoints for seamless tablet and smartphone learning.

## 📦 Deployment Guide
This project is configured for unified deployment on **Vercel**.
1. Push to GitHub.
2. Connect Repo to Vercel.
3. Add `MONGODB_URI` to Environment Variables.
4. Deploy!

---
*Built with ❤️ for the Professional Standards External Exam.*
=======
                                                                        # SkillCircle Full-Stack Project

This repository contains the code for the SkillCircle full-stack application.

## Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI, Pydantic
- Database: MongoDB

## Running the Application
### Backend
1. Open terminal and navigate to the `fastapi` folder
2. Install requirements using `pip install fastapi uvicorn pydantic "pymongo[srv]" dnspython`
3. Run using `python -m uvicorn main:app --reload`
4. The server runs on port 8000

### Frontend                                                                                                                                                                                                          
1. Make sure the backend server is running.
2. Serve the `frontend` folder using any local server, for example: `python -m http.server 5500`
3. Access `http://localhost:5500/welcome.html`
>>>>>>> 91b536e (commited)
