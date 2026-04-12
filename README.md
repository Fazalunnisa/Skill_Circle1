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
