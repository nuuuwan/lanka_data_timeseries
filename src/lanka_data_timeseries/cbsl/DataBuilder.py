import os
import tempfile

from utils import JSONFile, Log

from lanka_data_timeseries.cbsl.Config import Config
from lanka_data_timeseries.cbsl.FREQUENCY_LIST import FREQUENCY_LIST

log = Log(__name__)

SOURCE_ID = 'cbsl'


class DataBuilder:
    def __init__(self, d_idx: dict, d_footnote_idx: dict, config: Config):
        self.d_idx = d_idx
        self.d_footnote_idx = d_footnote_idx
        self.config = config

    @property
    def dir_data(self) -> str:
        dir_data = os.path.join(
            tempfile.gettempdir(), 'tmp.lanka_data_timeseries', 'sources', 'cbsl'
        )

        if not os.path.exists(dir_data):
            os.makedirs(dir_data)
            log.debug(f'Created {dir_data}')

        return dir_data

    @staticmethod
    def clean_time(t: str) -> str:
        t = t.replace('"', '')
        MONTHS = [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec',
        ]
        for i, month in enumerate(MONTHS):
            t = t.replace(month, f'{i+1:02d}')
        QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
        for i, quarter in enumerate(QUARTERS):
            m = (i + 1) * 3
            t = t.replace(quarter, f'{m:02d}')
        HALVES = ['H1', 'H2']
        for i, half in enumerate(HALVES):
            m = (i + 1) * 6
            t = t.replace(half, f'{m:02d}')

        if len(t) == 4:
            t = f'{t}-01-01'

        if len(t) == 7:
            t = f'{t}-01'

        return t

    @staticmethod
    def clean_value(x: str):
        x = x.replace('"', '')
        x = x.replace(' ', '')

        if x.startswith('(') and x.endswith(')'):
            x = '-' + x[1:-1]

        if x.lower() in ['...', '', '-', 'n.a', 'n.a.']:
            return None

        x = x.replace(',', '')
        x = x.replace('l', '1')
        x = x.replace('I', '1')
        x = x.replace("'", '')

        try:
            if '.' in x:
                return float(x)

            return int(x)

        except ValueError:
            log.warning(f'Could not clean {x}')

        return None

    @staticmethod
    def clean_data(t_to_value: dict[str, str]) -> dict[str,]:
        cleaned_d = dict(
            [
                (DataBuilder.clean_time(t), DataBuilder.clean_value(value))
                for t, value in t_to_value.items()
            ]
        )
        filtered_d = dict([x for x in cleaned_d.items() if x[1] is not None])
        sorted_d = dict(sorted(filtered_d.items(), key=lambda item: item[0]))

        return sorted_d

    @staticmethod
    def get_summary_statistics(d_data: dict) -> dict:
        t_list = list(d_data.keys())

        n = len(t_list)

        if n > 0:
            min_t = t_list[0]
            max_t = t_list[-1]
            min_value = d_data[min_t]
            max_value = d_data[max_t]
        else:
            min_t = None
            max_t = None
            min_value = None
            max_value = None

        return dict(
            n=n,
            min_t=min_t,
            max_t=max_t,
            min_value=min_value,
            max_value=max_value,
        )

    def write(self):
        frequency_name = self.config.frequency.name
        i_subject = self.config.i_subject

        for category, d_sub in self.d_idx.items():
            for sub_category, d_data in d_sub.items():
                log.debug(f'Writing {sub_category}...')
                raw_data = d_data['data']
                cleaned_data = DataBuilder.clean_data(raw_data)
                summary_statistics = DataBuilder.get_summary_statistics(
                    cleaned_data
                )

                footnotes = self.d_footnote_idx.get(sub_category, {})
                d_data_cleaned = dict(
                    source_id=SOURCE_ID,
                    category=category,
                    sub_category=sub_category,
                    scale=d_data['scale'],
                    unit=d_data['unit'],
                    frequency_name=frequency_name,
                    i_subject=i_subject,
                    footnotes=footnotes,
                    summary_statistics=summary_statistics,
                    cleaned_data=cleaned_data,
                    raw_data=raw_data,
                )

                file_name = os.path.join(
                    self.dir_data,
                    f'{SOURCE_ID}.{sub_category}.{frequency_name}.json',
                )
                JSONFile(file_name).write(d_data_cleaned)
                log.debug(f'Wrote {file_name}')


if __name__ == '__main__':
    print(DataBuilder.clean_time('2021-Jan'))
    print(DataBuilder.clean_time('2021-Dec'))
    print(DataBuilder.clean_time('2021-Q1'))
    print(DataBuilder.clean_time('2021-Q4'))
    print(DataBuilder.clean_time('2021-H1'))
    print(DataBuilder.clean_time('2021-H2'))

    print(DataBuilder.clean_value('1,000'))
    print(DataBuilder.clean_value('1,000.00'))
    print(DataBuilder.clean_value('l,000.00'))
    print(DataBuilder.clean_value('(1,000.00)'))

    print(
        DataBuilder.clean_data(
            {
                '2021-Q1': '1,000.00',
                '2021-01-07': '2,000.00',
                '2021-04': '3,000.00',
                '2021': 'None',
            }
        )
    )

    d_idx = {
        'A': {
            'B': {
                'scale': 'M',
                'unit': 'kg',
                'data': {
                    '2021-Q1': '1,000.00',
                    '2021-01-07': '2,000.00',
                    '2021-04': '3,000.00',
                },
            }
        }
    }
    d_footnote_idx = {
        'B': {
            'source': 'Finance Ministry',
            'sector': 'New Sector',
        }
    }
    DataBuilder(d_idx, d_footnote_idx, Config(FREQUENCY_LIST[0], 0)).write()
