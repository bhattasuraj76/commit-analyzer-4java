from pydriller import Repository
import re
import config
from helpers import get_file_ext

"""
  Analyze the target branch of the github repository and seperate added lines 
  and deleted lines of modified java files that match the function defination regex 
  into two separate lists for each commits. Compare the list to match function names and
  check if the added new function line increases the number of arguments
"""


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

                file_changes = file.diff
                # print(file.diff_parsed)

                overriding_func_sig_list = get_overriding_func(file_changes)
                overriden_func_sig_list = get_overriden_func(file_changes)
                print(overriding_func_sig_list, overriden_func_sig_list)
                for overriding_func in overriding_func_sig_list:
                    for overriden_func in overriden_func_sig_list:
                        # Get commits that added parameters to the exisiting function
                        # Changing > to != will yeild commits that modified the no of parameters to the existing function
                        if overriding_func[1] == overriden_func[1] and len(
                            overriding_func[2]
                        ) != len(overriden_func[2]):
                            results.append(
                                [
                                    commit_hash,
                                    filename,
                                    overriding_func[0],
                                    overriden_func[0],
                                ]
                            )

        # print(results)
        return results
    except Exception as e:
        raise e


#  Get list overriding function defination lines from file changes
def get_overriding_func(file_changes):
    raw_func_sig_list = []
    func_sig_list = []

    added_func_regex = config.regex["added_func_sign"]
    grp = re.finditer(added_func_regex, file_changes)
    raw_func_sig_list = [x.group() for x in grp]
    # print(raw_func_sig_list)

    for each in raw_func_sig_list:
        func_sign = trim_func_sign(each)
        func_name = get_func_name(func_sign)
        func_args = get_func_arguments(func_sign)
        func_sig_list.append([func_sign, func_name, func_args])

    # print(func_sig_list)
    return func_sig_list


#  Get list of overriden function defination from file changes
def get_overriden_func(file_changes):
    raw_func_sig_list = []
    func_sig_list = []

    deleted_func_regex = config.regex["deleted_func_sign"]
    matched_grp = re.finditer(deleted_func_regex, file_changes)
    raw_func_sig_list = [x.group() for x in matched_grp]
    # print(raw_func_sig_list)

    for each in raw_func_sig_list:
        func_sign = trim_func_sign(each)
        func_name = get_func_name(func_sign)
        func_args = get_func_arguments(func_sign)
        func_sig_list.append([func_sign, func_name, func_args])

    # print(func_sig_list)
    return func_sig_list


# Returns name of function from function signature
def get_func_name(func_sign):
    func_name_regex = "([a-zA-Z0-9_]+) *\\("
    # Match with function name regex
    func_name_search = re.search(func_name_regex, func_sign)
    func_name = trim_func_name(func_name_search.group())
    return func_name


# Returns list of function arguments from function signature
def get_func_arguments(func_sign):
    # Match with function arguments regex
    arg_search = re.search(config.regex["func_args"], func_sign)

    if arg_search is not None:
        func_args = trim_func_name(arg_search.group())
        func_args_list = func_args.split(",")
        return func_args_list
    else:
        return []


def trim_func_sign(func_sign):
    return func_sign.translate(func_sign.maketrans("", "", "+-{")).strip()


def trim_func_name(func_name):
    return func_name.translate(func_name.maketrans("", "", "()")).strip()
