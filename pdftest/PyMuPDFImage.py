import fitz  # PyMuPDF
import os

def extract_images_from_pdf(pdf_file, output_folder):
    # PDF 파일 열기
    pdf_document = fitz.open(pdf_file)

    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)

    # PDF의 모든 페이지에서 이미지 추출
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # 페이지 로드
        image_list = page.get_images(full=True)  # 이미지 목록 가져오기

        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # 이미지 확장자 추출 (예: 'png', 'jpeg')

            # 이미지 저장 경로 설정
            img_filename = f"page_{page_num + 1}_img_{image_index + 1}.{image_ext}"
            img_path = os.path.join(output_folder, img_filename)

            # 이미지 파일로 저장
            with open(img_path, 'wb') as img_file:
                img_file.write(image_bytes)
            print(f"이미지 저장: {img_path}")

# 사용 예시
pdf_file_path = "pdftest/input/pdf/금도끼와 은도끼.pdf"  # PDF 파일 경로
output_folder = "pdftest/imgFromPDF"  # 이미지를 저장할 폴더

# 함수 호출
extract_images_from_pdf(pdf_file_path, output_folder)
