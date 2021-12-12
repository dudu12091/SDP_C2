from pydriller import Repository
import pandas as pd
import numpy as np

commit_columns = ['Commit Hash', 'Commit Line Size', 'Commit File Size', 'Commit Timestamp', 'Commit Message',
                  'Add Tested Files', 'Add Test Files']
repos_columns = ['Repository Name', 'Commits Number', 'Bug Fixing Commits Number', 'Modified Lines', 'Modified Files',
                 'Commits metadata savepath']
repository_info = []


urls = pd.read_excel('ApacheRepository.xls')['Repository']

# for each repo using the Apache license...
for repo_url in urls:
    j = 0  # TODO: REMOVE THIS LIMITING NUMBER OF REPOS SO IT RUNS IN A REASONABLE TIME
    print("Mining from:", repo_url)

    repo = Repository(
        repo_url)  # TODO: which constraints should we add, if any? Dates? X amount of recent commits? All commits? Etc.
    bug_fix_count = 0
    modified_lines_num = 0
    modified_files_num = 0
    commit_num = 0
    commits_info = []
    # i = 0  # TODO: REMOVE THIS LIMITING NUMBER OF COMMITS SO IT RUNS IN A REASONABLE TIME

    # for each commit in this repo
    for commit in repo.traverse_commits():
        # ignore merge branch commits
        if commit.msg.lower().find('branch') > -1 and \
                (commit.msg.lower().find('merge') > -1 or commit.msg.lower().find('merging') > -1):
            pass

        # TODO: modify from print to story in a DF which can be converted to .csv outside of the loop
        # TODO: decide which metadata we want; currently just hash, msg and files changed for each commit
        commit_info = [commit.hash, commit.lines, commit.files, commit.committer_date, commit.msg]
        modified_lines_num += commit.lines
        modified_files_num += commit.files

        '''
        print("commit hash:", commit.hash)
        print("commit size (lines changed):", commit.lines)
        print("commit size (files changed):", commit.files)
        print("commit date:", commit.committer_date)
        '''

        # search bug fixing commits
        if (commit.msg.lower().find('bug') > -1 or commit.msg.lower().find('error') > -1)\
                and commit.msg.lower().find('fix') > -1:
            bug_fix_count += 1
            print("commit message:", commit.msg)

        commit_added_test_file = []
        commit_added_tested_file = []

        for file in commit.modified_files:
            if file.change_type.name == 'ADD' and file.filename.endswith('.java'):
                if file.filename.startswith('Test') or file.filename.endswith('Test.java'):
                    commit_added_test_file.append(file.filename)
                else:
                    commit_added_tested_file.append(file.filename)
        commit_info.append(commit_added_tested_file)
        commit_info.append(commit_added_test_file)
        commits_info.append(commit_info)

        commit_num += 1

    # save commits info
    repository_name = repo_url[repo_url.rfind('/') + 1: -4]
    commits_data_save_path = "repositoryMetadata/" + repository_name + '_commits_info.npy'
    commits_info = np.array(commits_info)
    np.save(commits_data_save_path, commits_info)

    # print('commits num: ', commit_num)
    # print('bug fix count: ', bug_fix_count)
    repository_info.append([repository_name, commit_num, bug_fix_count, modified_files_num,
                            modified_lines_num, commits_data_save_path])

    # TODO: REMOVE THIS LIMITING NUMBER OF REPOS SO IT RUNS IN A REASONABLE TIME
    j += 1
    if j > 3:
        break

repository_info = np.array(repository_info)
np.save('Repository_info.npy', repository_info)