import os
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from projects import projects_data

app = FastAPI()

# =============================
# CORS
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# STATIC
# =============================
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# =============================
# CACHE STATIC (tăng tốc load)
# =============================
from starlette.middleware.base import BaseHTTPMiddleware

class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        response = await call_next(request)

        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "public,max-age=31536000"

        return response

app.add_middleware(CacheControlMiddleware)

# =============================
# HOME
# =============================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    featured_projects = projects_data[:3]

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "featured_projects": featured_projects
        }
    )

# =============================
# PROJECTS LIST
# =============================
@app.get("/projects", response_class=HTMLResponse)
def projects(request: Request):

    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "projects": projects_data
        }
    )

# =============================
# PROJECT DETAIL (SEO SLUG)
# =============================
@app.get("/projects/{slug}", response_class=HTMLResponse)
def project_detail(request: Request, slug: str):

    project = next((p for p in projects_data if p["slug"] == slug), None)

    if not project:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    return templates.TemplateResponse(
        "project_detail.html",
        {
            "request": request,
            "project": project
        }
    )

# =============================
# REDIRECT OLD PROJECT ID
# =============================
@app.get("/projects/id/{project_id}")
def redirect_old_project(project_id: int):

    project = next((p for p in projects_data if p["id"] == project_id), None)

    if project:
        return RedirectResponse(
            url=f"/projects/{project['slug']}",
            status_code=301
        )

    return RedirectResponse("/projects")

# =============================
# ABOUT
# =============================
@app.get("/about", response_class=HTMLResponse)
def about(request: Request):

    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )

# =============================
# CONTACT PAGE
# =============================
@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):

    return templates.TemplateResponse(
        "contact.html",
        {"request": request}
    )

# =============================
# CONTACT SUBMIT
# =============================
@app.post("/contact-submit")
def contact_submit(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    location: str = Form(...),
    project_type: str = Form(...),
    budget: str = Form(...),
    message: str = Form(...),
):

    background_tasks.add_task(
        send_email_notify,
        name,
        phone,
        email,
        location,
        project_type,
        budget,
        message
    )

    return RedirectResponse("/contact-success", status_code=303)

# =============================
# CONTACT SUCCESS
# =============================
@app.get("/contact-success", response_class=HTMLResponse)
def contact_success(request: Request):

    return templates.TemplateResponse(
        "contact_success.html",
        {"request": request}
    )

# =============================
# NEWS
# =============================
@app.get("/news", response_class=HTMLResponse)
def news(request: Request):

    return templates.TemplateResponse(
        "news.html",
        {"request": request}
    )

# =============================
# EMAIL SEND
# =============================
def send_email_notify(name, phone, email, location, project_type, budget, message):

    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_RECEIVER")

    body = f"""
New client contact

Name: {name}
Phone: {phone}
Email: {email}
Location: {location}
Project: {project_type}
Budget: {budget}

Message:
{message}
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "New Contact Request"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()