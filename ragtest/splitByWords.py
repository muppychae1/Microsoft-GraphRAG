import os

def split_file_by_words(filename, num_parts):

    # 저장할 디렉토리 경로 설정
    input_dir = f'ragtest/input/{filename}'
    output_dir = 'ragtest/input/test/words'

    # 원본 파일을 읽기 모드로 열기 (UTF-8 인코딩 지정)
    with open(input_dir, 'r', encoding='utf-8') as file:
        text = file.read()  # 파일의 모든 내용을 읽어옴
    
    # 단어를 공백을 기준으로 분리
    words = text.split()
    
    # 전체 단어 수
    total_words = len(words)
    # 각 파일에 들어갈 단어 수
    words_per_file = total_words // num_parts
    # 남는 단어 수 계산 (작은 파일에 분배)
    remainder = total_words % num_parts

    print(f"전체 단어 수: {total_words}, 각 파일에 들어갈 단어 수: {words_per_file}, 남은 단어 수: {remainder}")

    start = 0
    for i in range(num_parts):
        # 종료 인덱스 설정
        end = start + words_per_file + (1 if i < remainder else 0)

        # 새로운 파일에 분할된 내용을 저장
        part_filename = f'{output_dir}/book_part_{10+i+1}.txt'

        with open(part_filename, 'w', encoding='utf-8') as part_file:
            part_file.write(' '.join(words[start:end]))
        
        # 다음 부분의 시작 인덱스 설정
        start = end

        # 생성된 파일의 크기 출력
        file_size = os.path.getsize(part_filename)

        # 생성된 파일의 단어 수 계산
        with open(part_filename, 'r', encoding='utf-8') as part_file:
            part_text = part_file.read()
            part_words = part_text.split()
            part_word_count = len(part_words)

        print(f"'{part_filename}' 파일의 크기: {file_size} 바이트, 단어 개수: {part_word_count}개")

    print(f"{num_parts}개의 파일로 '{filename}' 파일을 분할했습니다.")


def main() :
    # 사용 예시
    split_file_by_words('book2.txt', 10)
    

if __name__ == "__main__":
    main()