from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi import Form
import smtplib
from email.mime.text import MIMEText
import requests
import mysql.connector
from fastapi import BackgroundTasks
from projects import projects_data

from sqlalchemy import create_engine, text

db_url = "mysql+pymysql://root:@localhost/hplus_contact"
engine = create_engine(db_url)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
templates = Jinja2Templates(directory="templates")



# ==============================================
# HOME PAGE
# ==============================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Featured projects để hiển thị dưới hero section
    featured_projects = [
        {
            "id": 1,
            "name": "Casa Blanca Garden - Bến Tre",
            "category": "Villa garden",
            "cover": "/static/1.jpg",
        },
        {
            "id": 7,
            "name": "Tập Đoàn VFI", 
            "category": "Office",
            "cover": "/static/4.jpg",
        },
        {
            "id": 9,
            "name": "Happy Garden Retreat",
            "category": "resort",
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


@app.get("/projects", response_class=HTMLResponse)
def projects(request: Request):
    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "projects": projects_data
        }
    )

# ==============================================
# ABOUT PAGE
# ==============================================

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )

# ==============================================
# CONTACT PAGE
# ==============================================

@app.get("/admin/contacts")
def admin_contacts(request: Request):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    contacts = cursor.fetchall()

    return templates.TemplateResponse("admin_contacts.html", {
        "request": request,
        "contacts": contacts
    })


# ==============================================
# 404 CUSTOM (OPTIONAL)
# ==============================================

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse(
        "404.html",
        {"request": request},
        status_code=404
    )


@app.get("/projects/{ project.id }")
def project_detail(request: Request, project_id: int):
    project = next((p for p in projects_data if p["id"] == project_id), None)

    if not project:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )

    return templates.TemplateResponse(
        "project_detail.html",
        {
            "request": request,
            "project": project,
        }
    )

# ------------------
# NEWS DATA (ĐẶT TRÊN)
# ------------------

news_data = [

    {
        "id": 1,
        "title": "Dự án Casa Blanca Garden được đăng trên tạp chí ArchDaily",
        "thumbnail": "/static/news/1.jpg",
        "link": "https://www.archdaily.com/1028385/casa-blanca-garden-h2?ad_source=search&ad_medium=projects_tab",
        "date": "2024-10-21"
    },
    {
        "id": 2,
        "title": "Casa Blanca Garden Vinh Danh Top 10 Công Trình Xanh Của Năm 2025 ",
        "thumbnail": "/static/news/2.jpg",
        "link": "https://top10awards.vn/casa-blanca-garden-h-2/",
        "date": "2024-08-03"
    },
    {
        "id": 3,
        "title": "H+ Studio thắng giải Architecture MasterPrize 2024",
        "thumbnail": "/static/news/award1.jpg",
        "link": "https://architectureprize.com/winners-2024/",
        "date": "2024-09-12"
    },
]

@app.get("/news")
def news(request: Request):
    return templates.TemplateResponse(
        "news.html",
        {
            "request": request,
            "news_list": news_data
        }
    )


# ==========================
# MYSQL
# ==========================
# def save_to_database(name, phone, email, location, project_type, budget, message):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3306,
            password="",
            database="hplus_contact"
        )

        cursor = conn.cursor()

        sql = """
            INSERT INTO contacts (name, phone, email, location, project_type, budget, message)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (name, phone, email, location, project_type, budget, message)

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        print(">>> DB saved!")

    except Exception as e:
        print(">>> DB ERROR:", e)


# ==========================
# SEND EMAIL (GMAIL APP PASSWORD)
# ==========================


def send_email(subject, content):
    sender = "hplus.studio.vt@gmail.com"
    password = "ypxyaialerggdoxk"   # App password
    receiver = "hplus.studio.vt@gmail.com"

    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

# ==========================
# SEND ZALO
# ==========================
def send_zalo_notify(message):
    token = "0-SzFheLkn4FupSukHQn5mlZE3sx2irpGw8T3wmhybeTkYrnsINB8IAdG7JwKSq4DlidRkHDgpecudnmytUFNZxQGntnKufUAE9Y9Db8cdaqlHS0t23lTp2jFm29ECbhG9jQEeCJZ1PukNzYe0dt5M2O13k7A8vnOuDg4BeIXcXhf6y3s2srV1sQHLR6CQvqAyv27jjToLeE-HeumtNi5Z3xApp6UkrATj067uTrYM8hs68-o2hhJWw0E3xbFRvY4ObeDEWz-neCe0SruZxpLoYy7Zp0FFTr8AmbNV4qgmf6Yc5XYZZlCZgs1qNL9ieK4x4ZGA4OzdPKxJ4wv63aQZ3L0ZFxUVKS5OiVSC4dmm0Nq3HP_t3a4qZVD5AQJ-9zLUulEP5mn6nqsKukfL_3V4BH1nUFP8rRWSU-6xOEi1C"

    url = "https://openapi.zalo.me/v2.0/oa/message"

    data = {
        "recipient": {"user_id": "2736242473318265174"},
        "message": {"text": message}
    }

    headers = {
        "Content-Type": "application/json",
        "access_token": token
    }

    res = requests.post(url, json=data, headers=headers).json()
    print("Zalo notify:", res)


# ==========================
# CONTACT PAGE
# ==========================
@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "site_key": "6LfptXosAAAAAOGYwpvi3Fwe8rc-d9NAfa-RlFWK"
        }
    )


@app.post("/contact-submit")
def contact_submit(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    location: str = Form(...),
    project_type: str = Form(...),
    budget: str = Form(...),
    message: str = Form(...),
    captcha_token: str = Form(..., alias="g-recaptcha-response")
):

    # Gửi nhiệm vụ vào background
    background_tasks.add_task(
        process_contact_background,
        name, phone, email, location, project_type, budget, message, captcha_token
    )

    # Redirect KHÔNG CHỜ xử lý
    return RedirectResponse("/contact-success", status_code=303)


@app.get("/contact-success", response_class=HTMLResponse)
def contact_success(request: Request):
    return templates.TemplateResponse("contact_success.html", {"request": request})


def process_contact_background(name, phone, email, location, project_type, budget, message, captcha_token):
    

    try:
        # STEP 1: EMAIL
        print(">>> STEP 1: Sending email...")
        email_body = f"""
Khách hàng mới gửi yêu cầu tư vấn:

Tên: {name}
SĐT: {phone}
Email: {email}
Vị trí: {location}
Loại công trình: {project_type}
Ngân sách: {budget}
Nội dung: {message}
"""
        send_email("Yêu cầu tư vấn mới", email_body)
        print(">>> Email OK")

        # STEP 2: SAVE DB
        print(">>> STEP 2: Saving DB...")
        save_to_database(name, phone, email, location, project_type, budget, message)
        print(">>> DB OK")

        # STEP 3: ZALO
        print(">>> STEP 3: Sending Zalo notify...")
        send_zalo_notify("🔔 Có khách hàng mới gửi yêu cầu tư vấn!")
        print(">>> Zalo OK")

    except Exception as e:
        print(">>> ERROR in background task:", e)

@app.get("/test")
def test():
    return {"status": "ok"}