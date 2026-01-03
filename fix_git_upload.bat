@echo off
echo ====================================
echo FIX GIT UPLOAD ERRORS
echo ====================================
echo.

echo [1] Removing old git setup...
rd /s /q .git 2>nul

echo [2] Initializing new git repository...
git init

echo [3] Setting up git configuration...
git config user.email "claire19186-create@github.com"
git config user.name "claire19186-create"

echo [4] Connecting to GitHub...
git remote add origin https://github.com/claire19186-create/finance-research-classifier.git

echo [5] Pulling existing files from GitHub...
git pull origin main --allow-unrelated-histories

echo [6] Adding all project files...
git add .

echo [7] Checking what will be uploaded...
echo.
git status
echo.

echo [8] Committing changes...
git commit -m "Upload complete finance research classifier: app.py, src/, requirements.txt"

echo [9] Pushing to GitHub...
git push -u origin main

echo.
echo ====================================
echo ? UPLOAD SUCCESSFUL!
echo ====================================
echo.
echo Check your GitHub:
echo https://github.com/claire19186-create/finance-research-classifier
echo.
echo Then deploy to Streamlit Cloud!
echo.
pause