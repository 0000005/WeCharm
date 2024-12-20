@echo off
echo Starting build process...

echo Step 1: Building frontend...
cd frontend
call npm run build

echo Step 2: Copying dist files to backend/static...
xcopy /E /I /Y dist ..\backend\static\chat-app

echo Step 3: Building executable...
cd ..
python -m PyInstaller wecharm.spec --noconfirm --clean

echo Build process completed!
