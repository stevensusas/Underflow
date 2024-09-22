from github import Github
import base64
import mimetypes

# Provide your GitHub token (if needed) or use anonymous access
g = Github()

# Specify the repository by owner and name (e.g., "owner/repo")
repo = g.get_repo("stevensusas/MEAnalysis")

# Get the repository tree for the correct branch (e.g., 'main' or 'master')
contents = repo.get_contents("", ref="master")  # Change 'master' if the repo uses a different branch

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

# Variable to hold the concatenated content of all text files
concatenated_content = ""

# Loop through and read the content of each file
for file in all_files:
    print(f"Reading file: {file.path}")
    
    # Guess the file type
    mime_type, _ = mimetypes.guess_type(file.path)
    
    # Process only text files (skip binary files like images or PDFs)
    if mime_type and mime_type.startswith("text"):
        try:
            # Read and decode the file's content as text
            file_data = base64.b64decode(file.content).decode('utf-8')
            # Concatenate the content
            concatenated_content += file_data + "\n"  # Adding newline for separation between files
        except UnicodeDecodeError as e:
            print(f"Skipping file due to decode error: {file.path} - {e}")
    else:
        print(f"Skipping non-text file: {file.path}")

# Output the concatenated content
print("Concatenated content of all text files:")
print(concatenated_content)
