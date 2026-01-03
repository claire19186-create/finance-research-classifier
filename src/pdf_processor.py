# src/pdf_processor.py
import pdfplumber
import re

class PDFProcessor:
    def extract_text(self, pdf_file, max_pages=5):
        """
        Extract text from PDF (first few pages)
        """
        text = ""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for i, page in enumerate(pdf.pages[:max_pages]):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"--- Page {i+1} ---\n{page_text}\n\n"
        except Exception as e:
            text = f"Error extracting PDF: {str(e)}\n\n"
            text += "Make sure pdfplumber is installed: pip install pdfplumber"
        
        return text
    
    def extract_abstract(self, text):
        """
        Try to find abstract section in research paper
        """
        # Remove page markers first
        text = re.sub(r'--- Page \d+ ---\n', '', text)
        
        patterns = [
            r'Abstract\s*\n(.*?)(?=\n\s*\nIntroduction|$)',
            r'ABSTRACT\s*\n(.*?)(?=\n\s*\nINTRODUCTION|$)',
            r'Summary\s*\n(.*?)(?=\n\s*\n1\.|$)',
            r'abstract\s*\n(.*?)(?=\n\s*\n1\.|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                abstract = match.group(1).strip()
                # Clean up
                abstract = re.sub(r'\n+', ' ', abstract)
                abstract = re.sub(r'\s+', ' ', abstract)
                return abstract[:300] + "..." if len(abstract) > 300 else abstract
        
        # Fallback: first 300 characters
        if len(text) > 300:
            return text[:300] + "..."
        return text
    
    def count_words(self, text):
        """Count words in text"""
        # Remove page markers and extra whitespace
        clean_text = re.sub(r'--- Page \d+ ---\n', '', text)
        words = clean_text.split()
        return len(words)