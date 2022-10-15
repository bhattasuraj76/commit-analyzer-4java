import os

from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Url to github repository to be analyzed
target_repo_url = os.getenv("GITHUB_REPO_URL", None)

# Branch of the git repository that will be analyzed
target_branch = os.getenv("GIT_BRANCH", "main")

# Directory in the project root where resulting csv file gets created
output_dir = os.getenv("OUTPUT_DIR", "./output")

# Valid java file extensions
valid_file_ext = ["java"]


# Regular expressions
regex = {
    "added_func_sign": "\+ + (public|private|static|protected|abstract|native) ([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{",
    "deleted_func_sign": "- + (public|private|static|protected|abstract|native) ([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{",
    "func_args": "\(.*\)",
}
