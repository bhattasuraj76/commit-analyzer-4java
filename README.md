# commit-analyzer-4java
Analyzes the git commits in the java project that override the pre-existing function definations

## Getting Started

To run the project, python should be installed on your machine. 
Check if it is installed or not using 
 ```
 python --version
 ```

If it is not installed, download and install python from https://www.python.org/downloads/

Then, clone the repository:

````
git clone https://github.com/bhattasuraj76/commit-analyzer-4java.git
cd commit-analyzer-4java
````

Then, setup virtual environment (optional)
```
python3 -m venv venv
source venv/bin/activate
````

Then, install the requirements:
```
pip install -r requirements.txt
```

Create a .env file and copy the contents of .env.example
A dummy .env file will looking something like:
````
#content of .env file

GITHUB_REPO_URL=https://github.com/bhattasuraj76/test-java
GIT_BRANCH=origin/new-branch
# Use orign/<branch_name> if you want to use branches other that default master/main branch of git repo 
OUTPUT_DIR=hello
````
