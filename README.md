# commit-analyzer-4java
Analyzes the git commits in the java project that override the pre-existing function definations.
A `<repo-name>.csv` file with rows containing `commit sha`, `filename`, `old function signature`, `new function signature`
is generated.

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


`GITHUB_REPO_URL` : Url of the github repository(java-project) to be analyzed.   
`GIT_BRANCH` : Branch of the github repository to be analyzed.  
`OUTPUT_DIR` : Directory in the project root that will contain csv file  


Note : `GIT_BRANCH` should be a valid github repository branch. The default branch of github repository usually either `main` or `master`. Configure accordingly in the `.env` file. Branches other that default `main` or `master` should be written as `origin/<branch-name>`.


## OUTPUT
The project has been used to analyze two of the popular open source java projects: 
- https://github.com/square/okhttp.git
- https://github.com/square/picasso.git

The generated csv files(okhttp.csv and picasso.csv) are located inside `output` directory.