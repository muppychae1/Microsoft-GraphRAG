import subprocess
import time
import os
import yaml


# settings.yaml에서 input의 file_pattern 변경해줘야 함

def get_next_session_dir(base_path="ragtest/output"):
    # Find the highest numbered 'book_session_' directory in the output folder
    session_dirs = [d for d in os.listdir(base_path) if d.startswith("book_session_")]
    if session_dirs:
        last_session_num = max([int(d.split('_')[-1]) for d in session_dirs])
        next_session_num = last_session_num + 1
    else:
        next_session_num = 1
    return f"book_session_{next_session_num}"


def update_base_dir_in_settings():
    # Path to the settings.yaml file
    settings_path = "ragtest/settings.yaml"

    # Load the settings.yaml file with UTF-8 encoding
    with open(settings_path, 'r', encoding='utf-8') as file:
        settings = yaml.safe_load(file)

    # Generate the next session directory name
    next_session_dir = get_next_session_dir()

    # Update the base_dir inside the storage section
    settings['storage']['base_dir'] = f"output/{next_session_dir}/artifacts"
    settings['reporting']['base_dir'] = f"output/{next_session_dir}/reports"

    # Save the updated settings back to the file with UTF-8 encoding
    with open(settings_path, 'w', encoding='utf-8') as file:
        yaml.dump(settings, file, default_flow_style=False)

    print(f"Updated base_dir to: {settings['storage']['base_dir']}")


def timeCheck():
    # Record the start time
    start_time = time.time()
    print(f"Start Time: {time.ctime(start_time)}")

    # Execute the command
    subprocess.run(['python', '-m', 'graphrag.index', '--root', './ragtest'])

    # Record the end time
    end_time = time.time()
    print(f"End Time: {time.ctime(end_time)}")

    # Calculate and print the elapsed time
    elapsed_time = end_time - start_time
    print(f"Total Time Taken: {elapsed_time:.2f} seconds")


def main():
    # update_base_dir_in_settings()
    timeCheck()


if __name__ == "__main__":
    main()
