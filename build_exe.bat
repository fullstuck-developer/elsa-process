@echo off
echo ====================================================
echo    CAI DAT VA DONG GOI TOOL SUSPEND BLOCKER
echo ====================================================
echo.
echo 0. Chuan bi thu vien (Tu dong fix loi cho Python 3.13)...
echo psutil > requirements.txt
echo keyboard >> requirements.txt
echo pystray >> requirements.txt
echo Pillow >> requirements.txt

echo 1. Cai dat thu vien...
py -m pip install -r requirements.txt
py -m pip install pyinstaller
echo.
echo 2. Dang dong goi thanh file .exe...
py -m PyInstaller --name Elsa --noconsole --onefile --add-data "ice_emoji.png;." --icon NONE main.py
echo.
echo ====================================================
echo DONE! Vui long kiem tra trong thu muc "dist" da co file Elsa.exe chua.
echo ====================================================
pause
