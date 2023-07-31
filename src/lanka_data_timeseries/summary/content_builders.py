import os

from utils import File, JSONFile, Log, Time, TimeFormat

from src.lanka_data_timeseries.constants import DIR_TMP_DATA

log = Log(__name__)


def build_combined_summary(combined_summary_data_list):
    file_path = os.path.join(DIR_TMP_DATA, 'summary.json')
    JSONFile(file_path).write(combined_summary_data_list)
    file_size = os.path.getsize(file_path) / 1_000_000
    log.info(
        f'Wrote {len(combined_summary_data_list)} data items'
        + f' to "{file_path}" ({file_size:.2f}MB)'
    )
    return combined_summary_data_list


def get_source_to_n(combined_summary_data_list):
    source_to_n = {}
    for d in combined_summary_data_list:
        source_id = d['source_id']
        if source_id not in source_to_n:
            source_to_n[source_id] = 0
        source_to_n[source_id] += 1

    return source_to_n


def build_readme_source_summary(
    combined_summary_data_list: list,
) -> list[str]:
    lines = []
    source_to_n = get_source_to_n(combined_summary_data_list)
    for source, n in source_to_n.items():
        lines.append(f'* {source}: {n:,} datasets')
    n_all = len(combined_summary_data_list)
    lines.append(f'* TOTAL: **{n_all:,}** datasets')

    time_str = TimeFormat('%I:%M %p, %A, %d %B, %Y').stringify(Time.now())
    lines += [
        '',
        f'Last Updated: **{time_str}**',
        '',
    ]
    return lines


def build_readme_latest_updates(
    combined_summary_data_list: list,
) -> list[str]:
    lines = ['## Latest updates', '']
    sorted_combined_summary_data_list = sorted(
        combined_summary_data_list,
        key=lambda x: x['last_updated_time_ut'],
        reverse=True,
    )
    N_DISPLAY = 100
    for d in sorted_combined_summary_data_list[:N_DISPLAY]:
        source_id = d['source_id']
        sub_category = d['sub_category']
        frequency_name = d['frequency_name']
        last_updated_time_str = d['last_updated_time_str']
        lines.append(
            f'* {last_updated_time_str} - {sub_category}'
            + f' ({source_id} - {frequency_name})'
        )
    return lines


def build_readme(combined_summary_data_list: list):
    lines = [
        '# Lanka Data Timeseries',
        '*Public Timeseries Data about Sri Lanka*',
        '',
    ]

    lines += build_readme_source_summary(combined_summary_data_list)
    lines += build_readme_latest_updates(combined_summary_data_list)

    file_path = os.path.join(DIR_TMP_DATA, 'README.md')
    File(file_path).write_lines(lines)
    log.info(f'Wrote {file_path}')
    log.debug('\n'.join(lines))
