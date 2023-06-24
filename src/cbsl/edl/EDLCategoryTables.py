import os

from utils import Log, TSVFile

from cbsl.edl.EDLData import DIR_TMP_DATA, EDLData

log = Log(__name__)

DIR_CATEGORY_TABLES = os.path.join(DIR_TMP_DATA, 'category_tables')


class EDLCategoryTables(EDLData):
    @staticmethod
    def get_idx():
        d_list = EDLCategoryTables.get_data_list()
        idx = {}
        for d in d_list:
            category = d['category']
            sub_category = d['sub_category']
            scale = d['scale']
            unit = d['unit']
            cleaned_inner_data = d['cleaned_inner_data']

            if category not in idx:
                idx[category] = dict(
                    scale=scale, unit=unit, sub_category_to_data={}
                )
            idx[category]['sub_category_to_data'][
                sub_category
            ] = cleaned_inner_data

        return idx

    @staticmethod
    def init_dir():
        if not os.path.exists(DIR_CATEGORY_TABLES):
            os.makedirs(DIR_CATEGORY_TABLES)
            log.debug(f'Created {DIR_CATEGORY_TABLES}')

    @staticmethod
    def build():
        EDLCategoryTables.init_dir()

        idx = EDLCategoryTables.get_idx()
        for category, d_sub in idx.items():
            d_list = []
            for sub_category, cleaned_inner_data in d_sub[
                'sub_category_to_data'
            ].items():
                d = dict(sub_category=sub_category, **cleaned_inner_data)
                d_list.append(d)
            tsv_path = os.path.join(DIR_CATEGORY_TABLES, f'{category}.tsv')
            TSVFile(tsv_path).write(d_list)
            log.info(f'Wrote to {tsv_path}')
