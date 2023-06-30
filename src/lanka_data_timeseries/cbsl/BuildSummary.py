import os
import tempfile

from utils import Git, JSONFile, Log

log = Log(__name__)
URL_GIT_REPO = 'https://github.com/nuuuwan/lanka_data_timeseries.git'
DIR_TMP_DATA = os.path.join(
    tempfile.gettempdir(), 'tmp.lanka_data_timeseries'
)
BRANCH_DATA = 'data'


class BuildSummary:
    @staticmethod
    def get_data_list():
        git = Git(URL_GIT_REPO)
        git.clone(DIR_TMP_DATA, force=False)
        git.checkout(BRANCH_DATA)

        dir_data = os.path.join(DIR_TMP_DATA, 'sources', 'cbsl')
        d_list = []
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
            d_list.append(d)

        d_list = sorted(
            d_list, key=lambda x: x['sub_category'] + x['frequency_name']
        )
        n = len(d_list)
        log.debug(f'Found {n} data items')

        return d_list

    @staticmethod
    def extract(d):
        del d['raw_data']
        del d['cleaned_data']
        d['latest_value'] = d['summary_statistics']['max_value']
        return d

    @staticmethod
    def write(data_list_all):
        data_list = [BuildSummary.extract(d) for d in data_list_all]
        file_path = os.path.join(
            DIR_TMP_DATA, 'sources', 'cbsl', 'summary.json'
        )
        JSONFile(file_path).write(data_list)
        file_size = os.path.getsize(file_path) / 1_000_000
        log.info(
            f'Wrote {len(data_list)} data items to "{file_path}" ({file_size:.2f}MB)'
        )

    @staticmethod
    def build():
        data_list = BuildSummary.get_data_list()
        BuildSummary.write(data_list)


if __name__ == '__main__':
    BuildSummary.build()
