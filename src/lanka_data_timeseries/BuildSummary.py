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
    def init():
        git = Git(URL_GIT_REPO)
        git.clone(DIR_TMP_DATA, force=False)
        git.checkout(BRANCH_DATA)

    @staticmethod
    def get_source_id_list():
        dir_sources = os.path.join(DIR_TMP_DATA, 'sources')
        source_id_list = []
        for file_name_only in os.listdir(dir_sources):
            if os.path.isdir(os.path.join(dir_sources, file_name_only)):
                source_id_list.append(file_name_only)
        return source_id_list

    @staticmethod
    def get_data_list(source_id):
        dir_data = os.path.join(DIR_TMP_DATA, 'sources', source_id)
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
        return d

    @staticmethod
    def write(data_list_all, source_id):
        data_list = [BuildSummary.extract(d) for d in data_list_all]
        file_path = os.path.join(
            DIR_TMP_DATA, 'sources', source_id, 'summary.json'
        )
        JSONFile(file_path).write(data_list)
        file_size = os.path.getsize(file_path) / 1_000_000
        log.info(
            f'Wrote {len(data_list)} data items'
            + f' to "{file_path}" ({file_size:.2f}MB)'
        )

    @staticmethod
    def build():
        BuildSummary.init()
        source_id_list = BuildSummary.get_source_id_list()
        for source_id in source_id_list:
            data_list = BuildSummary.get_data_list(source_id)
            BuildSummary.write(data_list, source_id)


if __name__ == '__main__':
    BuildSummary.build()
