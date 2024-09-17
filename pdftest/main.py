import PyPDF2
import os

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text

def save_text_to_file(text, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

# 사용 예시
pdf_file_path = 'pdftest/input/15장 네트워크.pdf'  # PDF 파일 경로
pdf_text = extract_text_from_pdf(pdf_file_path)
save_text_to_file(pdf_text, 'pdftest/output/ExtractedText.txt')
