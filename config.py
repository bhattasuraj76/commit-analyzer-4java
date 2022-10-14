import os

from dotenv import load_dotenv

# Load env variables
load_dotenv()

target_repo_url = os.getenv("GITHUB_REPO_URL", None)
target_branch = os.getenv("GIT_BRANCH", "main")
output_dir = os.getenv("OUTPUT_DIR", "./output")

valid_file_ext = ["java"]
