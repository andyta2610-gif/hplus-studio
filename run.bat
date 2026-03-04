@echo off
echo ==== STARTING FASTAPI BACKEND ====
cd /d "D:\WEBSITE"
uvicorn main:app --reload
pause