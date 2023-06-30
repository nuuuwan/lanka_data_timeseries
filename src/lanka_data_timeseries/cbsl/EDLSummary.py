import os
import tempfile

from utils import JSONFile, Log

from lanka_data_timeseries.cbsl.EDLData import EDLData

DIR_TMP_DATA = os.path.join(
    tempfile.gettempdir(), 'tmp.lanka_data_timeseries'
)
log = Log(__name__)


class EDLSummary(EDLData):
    @staticmethod
    def build():
        d_list0 = EDLSummary.get_data_list()
        d_list = []
        for d in d_list0:
            del d['non_empty_inner_data']
            del d['cleaned_inner_data']
            d_list.append(d)

        json_path = os.path.join(DIR_TMP_DATA, 'cbsl_summary.json')
        JSONFile(json_path).write(d_list)
        log.info(f'Wrote to {json_path}')
