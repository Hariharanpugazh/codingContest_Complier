import os

def get_filepath():
    base_directory = 'compile/jsonfiles'
    problems_file_path = os.path.join(base_directory, 'problems.json')
    questions_file_path = os.path.join(base_directory, 'questions.json')

    # Check if problems.json exists; if not, use questions.json
    if os.path.exists(problems_file_path):
        PROBLEMS_FILE_PATH = problems_file_path
    else:
        PROBLEMS_FILE_PATH = questions_file_path
    
    return PROBLEMS_FILE_PATH