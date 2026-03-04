from database import SessionLocal
from models import User

db = SessionLocal()

users = db.query(User).all()

for u in users:
    print("Email:", u.email)
    print("Plan:", u.subscription_plan)
    print("Daily usage:", u.daily_usage)
    print("------")

db.close()
