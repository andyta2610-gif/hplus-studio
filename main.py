import os
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
import requests
from projects import projects_data

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# =============================
# HOME
# =============================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    featured_projects = [
        {
            "id": 1,
            "name": "Casa Blanca Garden",
            "category": "Villa garden",
            "cover": "/static/1.jpg",
        },
        {
            "id": 7,
            "name": "VFI Office",
            "category": "Office",
            "cover": "/static/4.jpg",
        },
        {
            "id": 9,
            "name": "Happy Garden Retreat",
            "category": "Resort",
            "cover": "/static/10.jpg",
        },
    ]

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "featured_projects": featured_projects
        }
    )

# =============================
# PROJECTS
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


@app.get("/projects/{project_id}", response_class=HTMLResponse)
def project_detail(request: Request, project_id: int):

    project = next((p for p in projects_data if p["id"] == project_id), None)

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
# ABOUT
# =============================
@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )

# =============================
# CONTACT
# =============================
@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {"request": request}
    )


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

    background_tasks.add_task(send_email_notify, name, phone, email, location, project_type, budget, message)

    return RedirectResponse("/contact-success", status_code=303)


@app.get("/contact-success", response_class=HTMLResponse)
def contact_success(request: Request):
    return templates.TemplateResponse(
        "contact_success.html",
        {"request": request}
    )

@app.get("/news", response_class=HTMLResponse)
def news(request: Request):
    return templates.TemplateResponse(
        "news.html",
        {"request": request}
    )
# =============================
# EMAIL
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
