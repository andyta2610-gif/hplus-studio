@echo off
setlocal enabledelayedexpansion
set count=1

for %%f in (*.png *.jpeg *.webp *.bmp *.gif) do (
    ren "%%f" "%%~nf.jpg"
    set /a count+=1
)
pause

