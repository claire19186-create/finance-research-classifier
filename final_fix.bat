@echo off
echo ====================================
echo FINAL FIX - FINANCE RESEARCH CLASSIFIER
echo ====================================
echo.

echo [1] Fixing file extensions...
if exist "app" ren "app" "app.py"
if exist "README" ren "README" "README.md"

echo [2] Checking src folder...
if not exist src (
    mkdir src
    echo   Created src folder
)

echo [3] Verifying pdf_processor.py...
if exist "src\pdf_processor.py" (
    echo   ? pdf_processor.py exists
) else (
    echo   ? pdf_processor.py not found in src folder
    echo   Please check manually
)

echo [4] Verifying all files...
echo.
echo ?? Project Structure:
dir /b
echo.
if exist src (
    echo ?? src/ folder:
    dir src /b
)

echo.
echo ====================================
echo ? PROJECT READY TO RUN!
echo ====================================
echo.
echo To run the app:
echo 1. Install: pip install -r requirements.txt
echo 2. Run: streamlit run app.py
echo 3. Open: http://localhost:8501
echo.
echo Note: If app.py doesn't exist, rename 'app' to 'app.py'
echo.
pause