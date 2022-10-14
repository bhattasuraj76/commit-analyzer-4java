from pydriller import Repository
import re
import config
from helpers import get_file_ext

def get_func_overriding_commits(repo_url, branch):
    try:
        results = []
        for commit in Repository(repo_url, only_in_branch=branch).traverse_commits():
            commit_hash = commit.hash

            for file in commit.modified_files:
                filename = file.filename

                # Check if file ext is valid java file ext
                fileext = get_file_ext(filename)
                if fileext not in config.valid_file_ext:
                    continue

                change = file.diff
                # print(file.diff_parsed)
                """ 
                func_def_list contains all the changed lines from git diff that gets matched against defined function regex
                in the format: 
                []
                """
                added_raw_func_def_list = []
                added_func_list = []
                deleted_raw_func_def_list = []
                deleted_func_list = []

                # Added code diff
                added_func_regex = "\+ + (public|private|static|protected|abstract|native) ([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{"
                grp = re.finditer(added_func_regex, change)
                added_raw_func_def_list = [x.group() for x in grp]
                # print(added_raw_func_def_list)

                func_name_regex = "([a-zA-Z0-9_]+) *\\("
                func_args_regex = "\(.*\)"
                for each in added_raw_func_def_list:
                    # Get function signature
                    func_sign = each.translate(each.maketrans("", "", "+{")).strip()

                    # Get function name
                    func_name_search = re.search(
                        func_name_regex, each
                    )  # Match with function name regex
                    func_name = func_name_search.group().strip(
                        "("
                    )  # Strip parentheis from matched string

                    # Get function list
                    arg_search = re.search(
                        func_args_regex, each
                    )  # Match with function arguments regex
                    if arg_search is not None:
                        func_args = (
                            arg_search.group().strip("(").strip(")")
                        )  # Strip parentheis from matched string
                        func_args_list = func_args.split(",")
                        added_func_list.append([func_sign, func_name, func_args_list])

                # print(added_func_list)

                # Deleted code diff
                deleted_func_regex = "- + (public|private|static|protected|abstract|native) ([a-zA-Z0-9<>._?, ]+) +([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\) *([a-zA-Z0-9_ ,\n]*) *\\{"
                grp = re.finditer(deleted_func_regex, change)
                deleted_raw_func_def_list = [x.group() for x in grp]
                # print(deleted_raw_func_def_list)

                func_name_regex = "([a-zA-Z0-9_]+) *\\("
                func_args_regex = "\(.*\)"
                for each in deleted_raw_func_def_list:
                    # Get function signature
                    func_sign = each.translate(each.maketrans("", "", "-{")).strip()

                    # Get function name
                    func_name_search = re.search(
                        func_name_regex, each
                    )  # Match with function name regex
                    func_name = func_name_search.group().strip(
                        "("
                    )  # Strip parentheis from matched string

                    # Get function list
                    arg_search = re.search(
                        func_args_regex, each
                    )  # Match with function arguments regex

                    if arg_search is not None:
                        func_args = (
                            arg_search.group().strip("(").strip(")")
                        )  # Strip parentheis from matched string
                        func_args_list = func_args.split(",")
                        deleted_func_list.append([func_sign, func_name, func_args_list])

                    # print(deleted_func_list)

                for x in added_func_list:
                    for y in deleted_func_list:
                        # Get commits that added parameters to the exisiting function 
                        # Changing > to != will yeild commits that modified the no of parameters to the existing function
                        if x[1] == y[1] and len(x[2]) != len(y[2]):
                            results.append([commit_hash, filename, x[0], y[0]])

        # print(results)
        return results
    except Exception as e:
        raise e
