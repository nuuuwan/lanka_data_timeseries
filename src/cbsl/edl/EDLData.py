import os
import tempfile

from utils import Git, JSONFile, Log

URL_GIT_REPO = 'https://github.com/nuuuwan/cbsl.git'
DIR_TMP_DATA = os.path.join(tempfile.gettempdir(), 'tmp.cbsl')
BRANCH_DATA = 'data'
log = Log(__name__)


class EDLData:
    @staticmethod
    def clean(x):
        x = x.replace(' ', '')

        if x.startswith('(') and x.endswith(')'):
            x = '-' + x[1:-1]
        if x.lower() in ['...', '', '-', 'n.a', 'n.a.']:
            return None

        x = x.replace(',', '')
        x = x.replace('l', '1')
        x = x.replace('I', '1')
        x = x.replace("'", '')

        if '.' in x:
            return float(x)

        return int(x)

    @staticmethod
    def filter_non_empty_data(inner_data):
        return dict(
            list(
                filter(
                    lambda x: x[1] is not None,
                    list(
                        map(
                            lambda x: [x[0], EDLData.clean(x[1])],
                            inner_data.items(),
                        )
                    ),
                )
            )
        )

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
        non_empty_inner_data = EDLData.filter_non_empty_data(inner_data)

        ts = list(non_empty_inner_data.keys())
        n = len(ts)
        min_t, max_t, latest_value = None, None, None
        if n > 0:
            min_t = min(ts)
            max_t = max(ts)
            latest_value = non_empty_inner_data[max_t]

        return dict(
            min_t=min_t,
            max_t=max_t,
            latest_value=latest_value,
            n=n,
            category=category,
            sub_category=sub_category,
            unit=unit,
            scale=scale,
            non_empty_inner_data=non_empty_inner_data,
        )

    @staticmethod
    def get_data_list():
        git = Git(URL_GIT_REPO)
        git.clone(DIR_TMP_DATA, force=False)
        git.checkout(BRANCH_DATA)

        dir_latest = os.path.join(DIR_TMP_DATA, 'latest')
        d_list = []
        for file_name_only in os.listdir(dir_latest):
            if not file_name_only.endswith('.json'):
                continue
            d = EDLData.get_d(file_name_only)
            d_list.append(d)

        d_list = sorted(
            d_list, key=lambda x: x['category'] + x['sub_category']
        )

        return d_list
