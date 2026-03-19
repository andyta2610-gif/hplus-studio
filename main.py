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

ZALO_ACCESS_TOKEN = "yANH6y7Ic1tyeTiTmj6I6_YXr1Z0pT5Q-UhO6RdDvdATnzqkzxt-Ji_AnX2MtO9XyT2gPvRwWoVorf4XrlQhVhFUw0lIwweKhTc9K-VYpnVN-CaIxltNUexQpG7qoUrUojxIAxJDzq_fnjGRbSpaUjlXx0ELrEvety7q59ZmrXJ0xPLyvFUd98lVusox_iOfujtPUQ_It0NGzl9KlSxEFkN3waJQxjmEXEQUHFU9km2fywTHmS2_LFt3j5QCruiCsgUv3OIIcdguiuam-eJ9GRkhvqRnel8PmBhnPQQUqJJ7fPXagR-hU-k_xndKdkr-v8xR7Bc4wHZQWlPhlxA-DEAWd5-3f8S1v8wwKhMAX1ZckzXptfNjT9_WnWUXm_zYsjx0DAlqd4BoqQOfblcITDZjZ29sH0b2SJBDoPCV"
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

    url = "https://openapi.zalo.me/v3.0/oa/message/cs"

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

    try:
        response = requests.post(url, json=payload, headers=headers)

        print("==== ZALO DEBUG ====")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

    except Exception as e:
        print("ZALO ERROR:", str(e))

# =============================
# ZALO WEBHOOK (NHẬN TIN NHẮN)
# =============================
from fastapi.responses import PlainTextResponse

@app.api_route("/zalo/webhook", methods=["GET", "POST"])
async def zalo_webhook(request: Request):

    if request.method == "GET":
        return PlainTextResponse("OK", status_code=200)

    try:
        data = await request.body()
        print("==== ZALO WEBHOOK ====")
        print(data)
    except Exception as e:
        print("ERROR:", str(e))

    return PlainTextResponse("OK", status_code=200)