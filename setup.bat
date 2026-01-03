@echo off
echo Creating all necessary files for Finance Research Classifier...
echo.

REM T?o requirements.txt
echo streamlit>=1.28.0 > requirements.txt
echo pandas>=2.0.0 >> requirements.txt
echo torch>=2.0.0 >> requirements.txt
echo plotly>=5.0.0 >> requirements.txt
echo numpy>=1.24.0 >> requirements.txt
echo pdfplumber>=0.10.0 >> requirements.txt
echo [?] Created requirements.txt

REM T?o LICENSE (MIT)
echo MIT License > LICENSE
echo. >> LICENSE
echo Copyright (c) 2024 Your Name >> LICENSE
echo. >> LICENSE
echo Permission is hereby granted... >> LICENSE
echo [?] Created LICENSE file

REM T?o .gitignore
echo __pycache__/ > .gitignore
echo *.py[cod] >> .gitignore
echo *$py.class >> .gitignore
echo *.so >> .gitignore
echo .Python >> .gitignore
echo build/ >> .gitignore
echo develop-eggs/ >> .gitignore
echo dist/ >> .gitignore
echo downloads/ >> .gitignore
echo eggs/ >> .gitignore
echo .eggs/ >> .gitignore
echo lib/ >> .gitignore
echo lib64/ >> .gitignore
echo parts/ >> .gitignore
echo sdist/ >> .gitignore
echo var/ >> .gitignore
echo wheels/ >> .gitignore
echo *.egg-info/ >> .gitignore
echo .installed.cfg >> .gitignore
echo *.egg >> .gitignore
echo .env >> .gitignore
echo .venv >> .gitignore
echo venv/ >> .gitignore
echo ENV/ >> .gitignore
echo env.bak/ >> .gitignore
echo venv.bak/ >> .gitignore
echo .streamlit/ >> .gitignore
echo [?] Created .gitignore file

REM T?o src/pdf_processor.py
if not exist src mkdir src
echo import pdfplumber > src/pdf_processor.py
echo import re >> src/pdf_processor.py
echo. >> src/pdf_processor.py
echo class PDFProcessor: >> src/pdf_processor.py
echo     def __init__(self): >> src/pdf_processor.py
echo         pass >> src/pdf_processor.py
echo. >> src/pdf_processor.py
echo     def extract_text(self, pdf_file, max_pages=3): >> src/pdf_processor.py
echo         '''Extract text from PDF''' >> src/pdf_processor.py
echo         text = '' >> src/pdf_processor.py
echo         try: >> src/pdf_processor.py
echo             with pdfplumber.open(pdf_file) as pdf: >> src/pdf_processor.py
echo                 for i, page in enumerate(pdf.pages[:max_pages]): >> src/pdf_processor.py
echo                     text += page.extract_text() + '\\n\\n' >> src/pdf_processor.py
echo         except Exception as e: >> src/pdf_processor.py
echo             raise Exception(f'PDF processing error: {str(e)}') >> src/pdf_processor.py
echo         return text >> src/pdf_processor.py
echo. >> src/pdf_processor.py
echo     def extract_abstract(self, text): >> src/pdf_processor.py
echo         '''Extract abstract section''' >> src/pdf_processor.py
echo         abstract_keywords = ['abstract', 'abstract:', 'summary', 'introduction'] >> src/pdf_processor.py
echo         lines = text.lower().split('\\n') >> src/pdf_processor.py
echo. >> src/pdf_processor.py
echo         for i, line in enumerate(lines): >> src/pdf_processor.py
echo             if any(keyword in line for keyword in abstract_keywords): >> src/pdf_processor.py
echo                 abstract = ' '.join(lines[i:i+10]) >> src/pdf_processor.py
echo                 return abstract[:1000] >> src/pdf_processor.py
echo. >> src/pdf_processor.py
echo         return text[:500] + '...' if len(text) > 500 else text >> src/pdf_processor.py
echo. >> src/pdf_processor.py
echo     def count_words(self, text): >> src/pdf_processor.py
echo         '''Count words in text''' >> src/pdf_processor.py
echo         return len(text.split()) >> src/pdf_processor.py
echo [?] Created src/pdf_processor.py

echo.
echo Setup complete! Files created:
echo - requirements.txt
echo - LICENSE
echo - .gitignore
echo - src/pdf_processor.py
echo.
echo Next steps:
echo 1. Run: pip install -r requirements.txt
echo 2. Run: streamlit run app.py
echo 3. Test your app!
pause