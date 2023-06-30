import os
import tempfile

from utils import Git, JSONFile, Log

log = Log(__name__)
URL_GIT_REPO = 'https://github.com/nuuuwan/lanka_data_timeseries.git'
DIR_TMP_DATA = os.path.join(
    tempfile.gettempdir(), 'tmp.lanka_data_timeseries'
)
BRANCH_DATA = 'data'


class BuildSuccessSummary:
    @staticmethod
    def get_idx():
        git = Git(URL_GIT_REPO)
        git.clone(DIR_TMP_DATA, force=True)
        git.checkout(BRANCH_DATA)

        dir_data = os.path.join(DIR_TMP_DATA, 'sources', 'cbsl')
        idx = {}
        for file_name_only in os.listdir(dir_data):
            if not file_name_only.endswith('.json'):
                continue
            if file_name_only in [
                'summary.json',
                '--log-success-summary.json',
            ]:
                continue

            file_path = os.path.join(dir_data, file_name_only)
            d = JSONFile(file_path).read()

            frequency_name = d['frequency_name']
            i_subject = d['i_subject']

            key = f'{frequency_name}-{i_subject:02d}'
            if key not in idx:
                idx[key] = 0
            idx[key] += 1

        idx = dict(sorted(idx.items(), key=lambda x: x[0]))
        return idx

    @staticmethod
    def write(idx):
        file_path = os.path.join(
            DIR_TMP_DATA, 'sources', 'cbsl', '--log-success-summary.json'
        )
        JSONFile(file_path).write(idx)
        log.info(f'Wrote "{file_path}"')

    @staticmethod
    def build():
        idx = BuildSuccessSummary.get_idx()
        BuildSuccessSummary.write(idx)
