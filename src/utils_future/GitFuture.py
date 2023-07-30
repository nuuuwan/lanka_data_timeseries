import time

import git
from utils import Time


class GitFuture:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)

    def get_last_update_ut(self, file_path: str) -> Time:
        commit = self.repo.iter_commits(
            paths=file_path, max_count=1
        ).__next__()
        return Time(time.mktime(commit.authored_datetime.timetuple()))
