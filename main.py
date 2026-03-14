import os
from news import news_data
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from projects import projects_data
from dotenv import load_dotenv

load_dotenv()

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

    # lấy project featured
    featured_projects = [p for p in projects_data if p.get("featured")]

    # chỉ lấy 3 project
    featured_projects = featured_projects[:3]

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
@app.get("/project/{project_id}")
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
        send_zalo_notify,
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
        {
            "request": request,
            "news_list": news_data
        }
    )

# =============================
# ZALO OA CONFIG
# =============================

import requests
from fastapi import Form, BackgroundTasks
from fastapi.responses import RedirectResponse

ZALO_ACCESS_TOKEN = "IjMh85sM4rL6qQ4cNfKPKqBHhYDSYNXJ2Q2HV1QV9sTOXkWI3xij54Mtus0choHNEPhdJ5wMNZerWx1ASw1nPIxdo4PGy0OoCCN5FdQ24meTXTi1VhKP5m7n-p9gp3f67SwAP7-EIszWjeva5u96KbMXyI0Rc44jNe6m812b0oPtij04BFrdDL3CeICexnWnIw3P7nA9Q3DoXumv6hOr24_oXG8cp5SYJl3WLHJMBbTeo-qWDkLUK47qlN8vytL-S-I-TJFvRqToegKo6h9a5LQAhXb8aNSINjA24WkLJmaIaeDz3eLW3bJAroCoxZ06QgZ0FZRfAH10zDCGFDWa9M2Tup0LZXi1IhRH452eV3e8kha-Hej032FAhNGz-t9HJTl5Ta_CCM03uF0JViGROndPqbO6cHzwBtQ0GL6D65S"
ZALO_USER_ID = "2736242473318265174"   # user đã từng chat với OA


# =============================
# SEND ZALO MESSAGE
# =============================

def send_zalo_notify(name, phone, email, location, project_type, budget, message):

    text = f"""
YÊU CẦU THIẾT KẾ MỚI

Họ tên: {name}
Điện thoại: {phone}
Email: {email}

Địa điểm: {location}
Loại công trình: {project_type}
Ngân sách: {budget}

Mô tả:
{message}
"""

    url = "https://openapi.zalo.me/v3.0/oa/message"

    payload = {
        "recipient": {
            "user_id": ZALO_USER_ID
        },
        "message": {
            "text": text
        }
    }

    headers = {
        "access_token": ZALO_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("ZALO STATUS:", response.status_code)
    print("ZALO RESPONSE:", response.text)