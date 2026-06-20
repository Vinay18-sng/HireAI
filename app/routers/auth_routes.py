from fastapi import APIRouter, Depends, HTTPException, status, Form, Response, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, crud, auth

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    company_name: str = Form(None),
    designation: str = Form(None),
    db: Session = Depends(get_db)
):
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email)
    if db_user:
        return RedirectResponse(url="/register?error=EmailAlreadyRegistered", status_code=303)
        
    try:
        # Create user schema
        user_create = schemas.UserCreate(name=name, email=email, password=password, role=role)
        # Create user
        new_user = crud.create_user(db, user_create)
        
        # Create profile based on role
        if role == "recruiter":
            if not company_name:
                company_name = "Self-Employed"
            recruiter_create = schemas.RecruiterCreate(
                company_name=company_name,
                designation=designation,
                user=user_create
            )
            crud.create_recruiter(db, recruiter_create, new_user.id)
        elif role == "candidate":
            crud.create_candidate_profile(db, new_user.id, name, email)
            
        return RedirectResponse(url="/login?message=AccountCreatedSuccessfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/register?error={str(e)}", status_code=303)


@router.post("/login")
async def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    next_url: str = Form(None, alias="next"),
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(db, email)
    if not db_user or not auth.verify_password(password, db_user.password_hash):
        # Redirect to login with error parameter
        redirect_url = "/login?error=InvalidCredentials"
        if next_url:
            redirect_url += f"&next={next_url}"
        return RedirectResponse(url=redirect_url, status_code=303)
        
    # Generate token
    token = auth.create_access_token(data={"sub": db_user.email})
    
    # Check where to redirect
    if next_url:
        redirect_to = next_url
    elif db_user.role == "admin":
        redirect_to = "/admin/dashboard"
    elif db_user.role == "recruiter":
        redirect_to = "/recruiter/dashboard"
    else:
        redirect_to = "/candidate/dashboard"
        
    response = RedirectResponse(url=redirect_to, status_code=303)
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=120 * 60, # 120 minutes
        expires=120 * 60,
        samesite="lax",
        secure=False  # Set to True in production with HTTPS
    )
    return response


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response
