import os
import tempfile

from utils import Git, JSONFile, Log, TSVFile

URL_GIT_REPO = 'https://github.com/nuuuwan/cbsl.git'
DIR_TMP_DATA = os.path.join(tempfile.gettempdir(), 'tmp.cbsl')
BRANCH_DATA = 'data'
log = Log(__name__)


class EDLSummary:
    @staticmethod
    def get_d(file_name_only):
        log.debug(f'Processing {file_name_only}...')
        tokens = file_name_only.split('.')
        category = tokens[0]
        sub_category = '.'.join(tokens[1:-1])

        file_path = os.path.join(DIR_TMP_DATA, 'latest', file_name_only)
        data = JSONFile(file_path).read()
        unit = data['unit']
        scale = data['scale']
        inner_data = data['data']
        non_empty_inner_data = dict(
            list(filter(lambda x: x[1].strip(), inner_data.items()))
        )
        ts = list(non_empty_inner_data.keys())
        n = len(ts)
        if n > 0:
            min_t = min(ts)
            max_t = max(ts)
            latest_value = non_empty_inner_data[max_t]
        else:
            min_t = None
            max_t = None
            latest_value = None

        return dict(
            min_t=min_t,
            max_t=max_t,
            latest_value=latest_value,
            n=n,
            category=category,
            sub_category=sub_category,
            unit=unit,
            scale=scale,
        )

    @staticmethod
    def build():
        git = Git(URL_GIT_REPO)
        git.clone(DIR_TMP_DATA, force=False)
        git.checkout(BRANCH_DATA)

        dir_latest = os.path.join(DIR_TMP_DATA, 'latest')
        d_list = []
        for file_name_only in os.listdir(dir_latest):
            if not file_name_only.endswith('.json'):
                continue
            d = EDLSummary.get_d(file_name_only)
            d_list.append(d)

        d_list = sorted(
            d_list, key=lambda x: x['category'] + x['sub_category']
        )

        tsv_path = os.path.join(DIR_TMP_DATA, 'edl_summary.tsv')
        TSVFile(tsv_path).write(d_list)
        log.info(f'Wrote to {tsv_path}')
