from pydriller import Repository
import pandas as pd
import numpy as np
import os
from git.repo import Repo


def calculate_TDD_metrics(commits_info):
    test_files = {}
    tested_files = {}
    before = 0
    same_time = 0
    after = 0
    for commit in commits_info:
        date = commit[COMMIT_TIMESTAMP]
        add_tested_files = commit[ADD_TESTED_FILES]
        add_test_files = commit[ADD_TEST_FILES]
        for file in add_tested_files:
            if tested_files.get(file, 0) == 0:
                tested_files[file] = date
        for file in add_test_files:
            if test_files.get(file, 0) == 0:
                test_files[file] = date
    pair_num = 0
    for file in test_files.items():
        test_date = file[1]
        if file[0].lower().startswith('test_'):
            tested_file_name = file[0][5:]
        elif file[0].lower().endswith('_test.java'):
            tested_file_name = file[0][:-10] + '.java'
        elif file[0].lower().startswith('test'):
            tested_file_name = file[0][4:]
        else:
            tested_file_name = file[0][:-9] + '.java'
        # a_Test, Test_a
        tested_date = tested_files.get(tested_file_name, None)
        if tested_date is not None:
            pair_num += 1
            if test_date < tested_date:
                before += 1
            elif test_date == tested_date:
                same_time += 1
            else:
                after += 1


    if pair_num != 0:
        p = float((before + same_time) / pair_num)
        before = float(before / pair_num)
        same_time = float(same_time / pair_num)
        after = float(after / pair_num)
    else:
        p = 0.0
        before = 0.0
        same_time = 0.0
        after = 0.0
    return p, before, same_time, after


commit_columns = ['Commit Hash', 'Commit Line Size', 'Commit File Size', 'Commit Timestamp', 'Commit Message',
                  'Add Tested Files Number', 'Add Test Files Number']
repos_columns = ['Repository Name', 'Stars', 'LOC', 'Size_Classification', 'Commits Number', 'Bug Fixing Commits Number',
                 'Modified Lines', 'Modified Files', 'Commits metadata savepath', 'TDD probability',
                 'Before Frequency', 'Same Commit Frequency', 'After Frequency']
COMMIT_HASH = 0
COMMIT_LINE_SIZE = 1
COMMIT_FILE_SIZE = 2
COMMIT_TIMESTAMP = 3
COMMIT_MESSAGE = 4
ADD_TESTED_FILES = 5
ADD_TEST_FILES = 6

repository_info = []

urls = pd.read_csv("k-Means/KMeansSplit_Control.csv")['Repository']
size_classes = pd.read_csv("k-Means/KMeansSplit_Control.csv")['Size_Classification']
stars = pd.read_csv("k-Means/KMeansSplit_Control.csv")['Stars']
locs = pd.read_csv("k-Means/KMeansSplit_Control.csv")['LOC']

urls = pd.read_csv("k-Means/kMeansSplit_Control.csv")["Repository"]

for i in range(28,29):
    print("Mining from:", urls[i])
    repository_name = urls[i][urls[i].rfind('/') + 1: -4]
    download_path = os.path.join('localRepos', repository_name)
    Repo.clone_from(urls[i], to_path=download_path)

    repo = Repository(download_path)  # TODO: which constraints should we add, if any? Dates? X amount of recent commits? All commits? Etc.
    bug_fix_count = 0
    modified_lines_num = 0
    modified_files_num = 0
    commit_num = 0
    commits_info = []

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

        commit_added_test_file = []
        commit_added_tested_file = []
        for file in commit.modified_files:
            if file.change_type.name == 'ADD' and file.filename.endswith('.java'):
                if file.filename.lower().startswith('test') or file.filename.lower().endswith('test.java'):
                    commit_added_test_file.append(file.filename)
                else:
                    commit_added_tested_file.append(file.filename)
        commit_info.append(commit_added_tested_file)
        commit_info.append(commit_added_test_file)
        commits_info.append(commit_info)

        commit_num += 1

    # save commits info
    p, before, same_time, after = calculate_TDD_metrics(commits_info)
    for commit_temp in commits_info:
        add_test_file = commit_temp.pop()
        add_tested_file = commit_temp.pop()
        commit_temp.append(len(add_tested_file))
        commit_temp.append(len(add_test_file))
    commits_data_save_path = "repositoryMetadata/" + repository_name + '_commits_info.npy'
    np.save(commits_data_save_path, commits_info)

    # print('commits num: ', commit_num)
    # print('bug fix count: ', bug_fix_count)
    repository_info.append([repository_name, stars[i], locs[i], size_classes[i], commit_num, bug_fix_count,
                            modified_files_num, modified_lines_num, commits_data_save_path,
                            p, before, same_time, after])

df = pd.DataFrame(repository_info, columns=repos_columns)
df.to_csv('Repository_info_2.csv')

