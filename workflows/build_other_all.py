from utils import Log

from lanka_data_timeseries.other_sources.adb import BuildData as BuildDataADB
from lanka_data_timeseries.other_sources.imf import BuildData as BuildDataIMF
from lanka_data_timeseries.other_sources.misc.multi_data import \
    BuildData as BuildDataMiscMulti
from lanka_data_timeseries.other_sources.misc.single_data import \
    BuildData as BuildDataMiscSingle
from lanka_data_timeseries.other_sources.world_bank import \
    BuildData as BuildDataWorldBank

log = Log(__file__)
if __name__ == '__main__':
    for BuildData in [
        BuildDataMiscMulti,
        BuildDataMiscSingle,
        BuildDataADB,
        BuildDataWorldBank,
        BuildDataIMF,
    ]:
        log.info('Running ' + BuildData.__name__)
        BuildData.build_data()
