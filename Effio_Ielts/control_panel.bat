@echo off
REM Render Control Panel Launcher
cd /d "D:\PYCODING\Quizz and test app\Effio_Ielts"

if "%1"=="" (
    echo Starting Render Control Panel...
    C:/Users/Admin/.virtualenvs/Quizz_and_test_app-bBUwlY-Z/Scripts/python.exe render_control_panel.py
) else (
    C:/Users/Admin/.virtualenvs/Quizz_and_test_app-bBUwlY-Z/Scripts/python.exe render_control_panel.py %1 %2
)