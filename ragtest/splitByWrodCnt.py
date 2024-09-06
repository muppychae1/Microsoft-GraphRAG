def split_text_file(input_file, output_prefix, words_per_file):
    # 저장할 디렉토리 경로 설정
    input_dir = f'ragtest/input/{input_file}'
    output_dir = 'ragtest/input/test/words'
    
    # Read the entire content of the input file
    with open(input_dir, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content into a list of words
    words = content.split()
    print(f"단어 총 개수: {len(words)}")
    
    # Calculate the total number of files needed
    total_files = (len(words) + words_per_file - 1) // words_per_file
    
    for i in range(total_files):
        # Determine the range of words for the current file
        start = i * words_per_file
        end = start + words_per_file
        
        # Create the content for the current file
        file_content = ' '.join(words[start:end])
        
        # Write the content to a new file
        output_file = f"{output_dir}/{output_prefix}_{i+1}.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(file_content)
        
        print(f"Created: {output_file}")

if __name__ == "__main__":
    input_file = 'book2.txt'         # Replace with your input file path
    output_prefix = 'book_part'    # Replace with your desired output file prefix
    words_per_file = 3500            # Replace with the desired number of words per file

    split_text_file(input_file, output_prefix, words_per_file)
