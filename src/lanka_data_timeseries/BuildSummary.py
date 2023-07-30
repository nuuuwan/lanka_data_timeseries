import os
import tempfile

from utils import TIME_FORMAT_TIME, File, Git, JSONFile, Log, Time, TimeFormat

from utils_future import GitFuture

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
        git_future = GitFuture(DIR_TMP_DATA)
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
            assert d['source_id'] == source_id

            ut = git_future.get_last_update_ut(file_path)
            d['last_updated_ut'] = ut
            d['last_updated_time'] = TIME_FORMAT_TIME.stringify(Time(ut))
            d_list.append(d)

        d_list = sorted(
            d_list, key=lambda x: x['sub_category'] + x['frequency_name']
        )
        len(d_list)
        return d_list

    @staticmethod
    def extract(d):
        del d['raw_data']
        del d['cleaned_data']
        return d

    @staticmethod
    def write(data_list_all, source_id):
        summary_data_list = [BuildSummary.extract(d) for d in data_list_all]
        file_path = os.path.join(
            DIR_TMP_DATA, 'sources', source_id, 'summary.json'
        )
        JSONFile(file_path).write(summary_data_list)
        file_size = os.path.getsize(file_path) / 1_000_000
        log.debug(
            f'Wrote {len(summary_data_list)} data items'
            + f' to "{file_path}" ({file_size:.2f}MB)'
        )
        return summary_data_list

    @staticmethod
    def build_individual_summaries():
        BuildSummary.init()
        source_id_list = BuildSummary.get_source_id_list()
        combined_summary_data_list = []
        for source_id in source_id_list:
            data_list = BuildSummary.get_data_list(source_id)
            summary_data_list = BuildSummary.write(data_list, source_id)
            combined_summary_data_list += summary_data_list
        return combined_summary_data_list

    @staticmethod
    def build_combined_summary(combined_summary_data_list):
        file_path = os.path.join(DIR_TMP_DATA, 'summary.json')
        JSONFile(file_path).write(combined_summary_data_list)
        file_size = os.path.getsize(file_path) / 1_000_000
        log.info(
            f'Wrote {len(combined_summary_data_list)} data items'
            + f' to "{file_path}" ({file_size:.2f}MB)'
        )
        return combined_summary_data_list

    @staticmethod
    def get_source_to_n(combined_summary_data_list):
        source_to_n = {}
        for d in combined_summary_data_list:
            source_id = d['source_id']
            if source_id not in source_to_n:
                source_to_n[source_id] = 0
            source_to_n[source_id] += 1

        return source_to_n

    @staticmethod
    def build_readme(combined_summary_data_list):
        lines = [
            '# Lanka Data Timeseries',
            '*Public Timeseries Data about Sri Lanka*',
            '',
        ]

        source_to_n = BuildSummary.get_source_to_n(combined_summary_data_list)
        for source, n in source_to_n.items():
            lines.append(f'* {source}: {n:,} datasets')
        n_all = len(combined_summary_data_list)
        lines.append(f'* TOTAL: **{n_all:,}** datasets')

        time_str = TimeFormat('%I:%M %p, %A, %d %B, %Y').stringify(Time.now())
        lines += [
            '',
            f'Last Updated: **{time_str}**',
        ]

        file_path = os.path.join(DIR_TMP_DATA, 'README.md')
        File(file_path).write_lines(lines)
        log.info(f'Wrote {file_path}')
        log.debug('\n'.join(lines))

    @staticmethod
    def build():
        combined_summary_data_list = BuildSummary.build_individual_summaries()
        BuildSummary.build_combined_summary(combined_summary_data_list)
        BuildSummary.build_readme(combined_summary_data_list)


if __name__ == '__main__':
    BuildSummary.build()
