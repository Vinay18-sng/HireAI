import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.auth import AuthRedirectException, get_current_user_optional
from app.routers import auth_routes, admin, recruiter, candidate, jobs, analytics

# Initialize FastAPI App
app = FastAPI(title="HireAI Platform", version="1.0.0")

# Exception handler for cookie auth redirects
@app.exception_handler(AuthRedirectException)
async def auth_redirect_exception_handler(request: Request, exc: AuthRedirectException):
    redirect_url = exc.redirect_url
    # Append message parameter to alert the user in UI
    if exc.message:
        connector = "&" if "?" in redirect_url else "?"
        redirect_url += f"{connector}error={exc.message}"
    return RedirectResponse(url=redirect_url, status_code=303)

# Create Database tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")
    
    # Ensure uploads directory exists
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_dir = os.path.join(base_dir, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    print(f"Uploads directory verified at: {upload_dir}")

    # Auto-seed if database is empty and auto-seeding is enabled
    if os.getenv("AUTO_SEED", "true").lower() == "true":
        try:
            from seed import auto_seed_if_empty
            auto_seed_if_empty()
        except Exception as e:
            print(f"Auto-seeding skipped or failed: {e}")

# Mount Static Files
static_path = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Templates Configuration
templates_path = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_path)

# Include Routers
app.include_router(auth_routes.router)
app.include_router(admin.router)
app.include_router(recruiter.router)
app.include_router(candidate.router)
app.include_router(jobs.router)
app.include_router(analytics.router)

# --- Base Landing Page Routes ---

@app.get("/")
async def index(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "current_user": current_user,
            "active_tab": "home"
        }
    )

@app.get("/login")
async def login_page(
    request: Request,
    current_user = Depends(get_current_user_optional)
):
    if current_user:
        # Redirect if already logged in
        if current_user.role == "admin":
            return RedirectResponse(url="/admin/dashboard")
        elif current_user.role == "recruiter":
            return RedirectResponse(url="/recruiter/dashboard")
        else:
            return RedirectResponse(url="/candidate/dashboard")
            
    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "current_user": None
        }
    )

@app.get("/register")
async def register_page(
    request: Request,
    current_user = Depends(get_current_user_optional)
):
    if current_user:
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse(
        request,
        "register.html",
        {
            "current_user": None
        }
    )
