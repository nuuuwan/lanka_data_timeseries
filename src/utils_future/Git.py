import os

from utils_base import Log

log = Log('Git')


class Git:
    @staticmethod
    def from_github(user_name: str, repo_name: str):
        return Git(f'https://github.com/{user_name}/{repo_name}.git')

    def __init__(self, git_repo_url: str):
        log.debug(f'Initializing Git({git_repo_url=})')
        self.git_repo_url = git_repo_url
        self.dir_repo = None
        self.branch_name = None

    def run(self, *cmd_lines: list[str]):
        assert self.dir_repo is not None
        cmd_lines = ['cd', self.dir_repo, '&&'] + list(cmd_lines)
        cmd = ' '.join(cmd_lines)
        log.debug(cmd)

        os.system(cmd)

    def __init_dir_repo__(self, dir_repo: str):
        self.dir_repo = dir_repo
        assert not os.path.exists(dir_repo)

        os.makedirs(dir_repo)
        log.info(f'Created {dir_repo}')

    # Initialization
    def clone(self, dir_repo: str, branch_name: str):
        # Clone (or copy) a repository from an existing URL.
        assert dir_repo is not None
        assert branch_name is not None

        if os.path.exists(dir_repo):
            log.warn(f'Using existing {dir_repo}. Not cloning.')
            return

        log.info(f'Cloning {self.git_repo_url=} to {dir_repo=}')
        self.__init_dir_repo__(dir_repo)
        self.branch_name = branch_name

        self.run(
            'git clone',
            '--single-branch',
            '--branch',
            self.branch_name,
            self.git_repo_url,
            self.dir_repo,
        )
