import os

from utils import JSONFile, Log

from lanka_data_timeseries.cbsl.Config import Config
from lanka_data_timeseries.common import clean_time, clean_value
from lanka_data_timeseries.common_statistics import get_summary_statistics
from lanka_data_timeseries.constants import DIR_TMP_DATA

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
            DIR_TMP_DATA,
            'sources',
            'cbsl',
        )

        if not os.path.exists(dir_data):
            os.makedirs(dir_data)
            log.debug(f'Created {dir_data}')

        return dir_data

    @staticmethod
    def clean_data(t_to_value: dict[str, str]) -> dict[str,]:
        cleaned_d = dict(
            [
                (clean_time(t), clean_value(value))
                for t, value in t_to_value.items()
            ]
        )
        filtered_d = dict([x for x in cleaned_d.items() if x[1] is not None])
        sorted_d = dict(sorted(filtered_d.items(), key=lambda item: item[0]))

        return sorted_d

    def write_sub_category(self, category, sub_category, d_data):
        frequency_name = self.config.frequency.name
        i_subject = self.config.i_subject

        raw_data = d_data['data']
        cleaned_data = DataBuilder.clean_data(raw_data)
        summary_statistics = get_summary_statistics(cleaned_data)

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

    def write(self):
        for category, d_sub in self.d_idx.items():
            for sub_category, d_data in d_sub.items():
                self.write_sub_category(category, sub_category, d_data)
