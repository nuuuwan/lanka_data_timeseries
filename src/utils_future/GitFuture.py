import git


class GitFuture:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)

    def get_last_update_time(self, file_path: str):
        index_entry = self.repo.index[file_path]
        commit = index_entry.commit
        last_update_time = commit.authored_datetime
        return last_update_time
