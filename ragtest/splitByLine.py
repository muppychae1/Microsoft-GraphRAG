import os

def split_file_by_lines(filename, num_parts):

    # 저장할 디렉토리 경로 설정
    input_dir = f'ragtest/input/{filename}'
    output_dir = 'ragtest/input/test/line'

    # 원본 파일을 읽기 모드로 열기 (UTF-8 인코딩 지정)
    with open(input_dir, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 모든 라인을 읽어 리스트로 저장
    
    # 전체 라인 수
    total_lines = len(lines)
    # 각 파일에 들어갈 라인 수 ( // : 몫만 반환 )
    lines_per_file = total_lines // num_parts
    # 남는 라인 수 계산 (작은 파일에 분배)
    remainder = total_lines % num_parts

    print(f"전체 라인 수: {total_lines}, 각 파일에 들어갈 라인 수: {lines_per_file}, 남은 라인 수: {remainder}")

    start = 0
    for i in range(num_parts):
        # 종료 인덱스 설정
        end = start + lines_per_file + (1 if i < remainder else 0)

        # 새로운 파일에 분할된 내용을 저장
        part_filename = f'{output_dir}/book_part_{i+1}.txt'

        with open(part_filename, 'w', encoding='utf-8') as part_file:
            part_file.writelines(lines[start:end])
        
        # 다음 부분의 시작 인덱스 설정
        start = end

        # 생성된 파일의 크기 출력
        file_size = os.path.getsize(part_filename)
        print(f"'{part_filename}' 파일의 크기: {file_size} 바이트")

    print(f"{num_parts}개의 파일로 '{filename}' 파일을 분할했습니다.")


def main() :
    # 사용 예시
    split_file_by_lines('book.txt', 10)
    

if __name__ == "__main__":
    main()