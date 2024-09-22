import click
import requests
from underflow_sdk.analyze_code import check_for_external_services
import json
import subprocess
import os
import webbrowser
import time
import requests
from github import Github
import base64
import mimetypes
import dotenv
import os
import pyautogui

DO_FRONTEND_STUFF = False

dotenv.load_dotenv()
# Set of file extensions that are commonly used for code files
CODE_FILE_EXTENSIONS = {
    ".py",
    ".js",
    ".java",
    ".c",
    ".cpp",
    ".cs",
    ".rb",
    ".php",
    ".go",
    ".ts",
    ".rs",
    ".swift",
}


def summarize_for_generation(code_str, recommendations):
    stream = False
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": os.getenv("TUNE_KEY"),
        "Content-Type": "application/json",
    }
    data = {
        "temperature": 0.8,
        "messages": [
            {
                "role": "system",
                "content": "Given a long code string and recommendations, give instructions to a machine on how to use those recommendations to generate new code. Write one single sentence, 20 words or less. Do not write more than 20 words. Make sure you are providing instructions to generatea code to a machine. ",
            },
            {
                "role": "user",
                "content": f"code string: {code_str}, recommendations: {recommendations}",
            },
        ],
        "model": "anthropic/claude-3-haiku",
        "stream": stream,
        "frequency_penalty": 0,
        "max_tokens": 900,
    }
    response = requests.post(url, headers=headers, json=data)
    msg = response.json()["choices"][0]["message"]["content"]
    return msg


def create_defang(instructions):
    subprocess.Popen("defang generate", shell=True)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")
    pyautogui.write(instructions, interval=0.01)
    pyautogui.press("enter")
    pyautogui.press("enter")


def get_repository(repository_name: str):
    print("Scanning your codebase...")
    # Provide your GitHub token (if needed) or use anonymous access
    g = Github(os.getenv("GITHUB_KEY"))

    # Specify the repository by owner and name (e.g., "owner/repo")
    repo = g.get_repo(repository_name)

    # Get the repository tree for the correct branch (e.g., 'main' or 'master')
    contents = repo.get_contents(
        "", ref="master"
    )  # Change 'master' if the repo uses a different branch

    def get_all_files(repo, contents):
        files = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                # If it's a directory, fetch its contents
                contents.extend(repo.get_contents(file_content.path))
            else:
                # Add the file path
                files.append(file_content)
        return files

    # Fetch all files
    all_files = get_all_files(repo, contents)

    # Variable to hold the concatenated content of all code files
    concatenated_content = ""

    # Loop through and read the content of each file
    for file in all_files:
        file_extension = os.path.splitext(file.path)[1]  # Extract file extension
        print(f"Checking file: {file.path}")

        # Only process files with code-related extensions
        if file_extension in CODE_FILE_EXTENSIONS:
            print(f"Reading code file: {file.path}")

            try:
                # Read and decode the file's content as text
                file_data = base64.b64decode(file.content).decode("utf-8")
                # Concatenate the content
                concatenated_content += (
                    file_data + "\n"
                )  # Adding newline for separation between files
            except UnicodeDecodeError as e:
                print(f"Skipping file due to decode error: {file.path} - {e}")
        else:
            print(f"Skipping non-code file: {file.path}")

    # Output the concatenated content of all code files
    print("Concatenated content of all code files:")
    print(concatenated_content)
    print("Codebase scan complete! Analyzing external services...")
    return concatenated_content


@click.command
@click.argument("repository")
@click.argument("traffic")
def cli(repository: str, traffic: int):
    code_str = get_repository(repository)
    resp = check_for_external_services(code_str=code_str, traffic=traffic)

    # create_defang()

    if DO_FRONTEND_STUFF:
        shell_command = f"cd ../../frontend/my-app && npm run dev"

        subprocess.Popen(shell_command, shell=True)

        time.sleep(3)

        try:
            webbrowser.open("http://localhost:3000")
        except Exception as e:
            print(f"Failed to launch browser: {e}")

    # print("Your original Tech Stack:" + json.dumps(resp[0], indent=4))
    # print("Your Optimized Tech Stack:" + json.dumps(resp[1], indent=4))
    # print("Technical Report:" + json.dumps(resp[2], indent=4))

    json_body = {}
    json_body["original_service"] = resp[0]
    json_body["optimal_service"] = resp[1]
    json_body["tech_report"] = resp[2]
    json_body["repository_name"] = repository
    resp = requests.post("http://127.0.0.1:8000/api/set_info", json=json_body)

    instructions = summarize_for_generation(
        code_str=code_str, recommendations=json_body["tech_report"]["report"]
    )
    print(instructions)
    create_defang(instructions=instructions)
