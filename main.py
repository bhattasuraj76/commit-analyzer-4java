import config
from helpers import get_repo_name, export_to_csv
from analyzer import get_func_overriding_commits

target_repo_url = config.target_repo_url
target_branch = config.target_branch
if target_repo_url:
    print(f"Repository URL: {target_repo_url}")
    try:
        headers = [
            "Hash",
            "Filename",
            "New Function Signature",
            "Old Function Signature",
        ]
        results = get_func_overriding_commits(target_repo_url, target_branch)
        filename = get_repo_name(target_repo_url)
        output_dir = config.output_dir
        export_to_csv(data=results, headers=headers, dir=output_dir, filename=filename)
        print(f"Successfully generated {filename}.csv iniside direcoty {output_dir}")

    except Exception as e:
        print(f"Error occured: {type(e).__name__}")
        print(str(e))
else:
    print("Github repository url not found in .env file")
