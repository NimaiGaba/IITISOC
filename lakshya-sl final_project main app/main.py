#python backend for connecting all 3 interfaces

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = FastAPI()

# Secret key is needed for session management.
# Load from environment variable or use a fallback for development.
SECRET = os.getenv("SESSION_SECRET", "a-very-secret-key-that-you-should-change")

# Add session middleware to handle user sessions
# This allows us to store information across requests
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET,
    same_site="lax",
    https_only=False # Set to True in production with HTTPS
)

# Mount directories to serve static files
# This makes files in these folders accessible via URL paths
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/login_page", StaticFiles(directory="login_page"), name="login_page")
app.mount("/after_login", StaticFiles(directory="after_login"), name="after_login")



@app.get("/", response_class=HTMLResponse)
def get_home():
    """Serves the main landing page (index.html)."""
    return FileResponse("index.html")

@app.get("/login", response_class=HTMLResponse)
def get_login_page():
    """Serves the login/signup page (page.html)."""
    return FileResponse("login_page/page.html")

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request):
    """
    Serves the protected user interface (ui.html).
    It check for a user session first. If no session is found,
    it redirects the user to the login page.
    """
    if not request.session.get("firebase_user"):
        # If no user is in the session, deny access and redirect
        return RedirectResponse(url="/login", status_code=302)
    # If a user session exists, serve the main UI
    return FileResponse("after_login/frontend/ui.html")

@app.post("/session-login")
async def create_session(request: Request):
    """
    This endpoint is called by the frontend JavaScript after a successful
    Firebase login. It creates a server-side session for the user.
    """
    try:
        body = await request.json()
        email = body.get("email")
        if email:
            # Store the user's email in the session
            request.session["firebase_user"] = email
            return {"status": "success", "message": "Session created"}
        return {"status": "error", "message": "Email not provided"}, 400
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@app.get("/logout")
def logout(request: Request):
    """Clears the user session and redirects to the login page."""
    request.session.clear()
    # Redirect to the login page instead of the homepage
    return RedirectResponse(url="/login", status_code=302)
