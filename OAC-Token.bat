@echo off
rem ============================================================
rem  OAC Token Manager - bam doi de mo app nap token OAC
rem  Dung khi: tai token moi tu OAC (Profile > Access Tokens > Download)
rem  Cach dung: mo app > "Chon file token..." > "NAP TOKEN". Xong.
rem ============================================================
title OAC Token Manager
set "GUI=%~dp0OAC-Knowledge\kb_lifecycle\tools\oac_token_gui.py"

if not exist "%GUI%" (
  echo [LOI] Khong tim thay: %GUI%
  echo Hay chay file .bat nay tu thu muc goc du an KGR-OAC-Agents.
  pause
  exit /b 1
)

rem Uu tien pythonw (khong hien cua so den). Neu loi thi chay python de thay thong bao.
where pythonw >nul 2>&1
if %errorlevel%==0 (
  start "" pythonw "%GUI%"
  exit /b 0
)

echo Khong thay pythonw, dang chay bang python...
python "%GUI%"
if errorlevel 1 pause
