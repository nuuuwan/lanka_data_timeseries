import os
import tempfile

from utils import Log, TSVFile

from cbsl.edl.EDLData import EDLData

URL_GIT_REPO = 'https://github.com/nuuuwan/cbsl.git'
DIR_TMP_DATA = os.path.join(tempfile.gettempdir(), 'tmp.cbsl')
BRANCH_DATA = 'data'
log = Log(__name__)


class EDLSummary(EDLData):
    @staticmethod
    def build():
        d_list0 = EDLSummary.get_data_list()
        d_list = []
        for d in d_list0:
            del d['non_empty_inner_data']
            d_list.append(d)

        tsv_path = os.path.join(DIR_TMP_DATA, 'edl_summary.tsv')
        TSVFile(tsv_path).write(d_list)
        log.info(f'Wrote to {tsv_path}')
