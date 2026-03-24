from utils import Log

from lanka_data_timeseries.other_sources.adb import BuildData as BuildDataADB
from lanka_data_timeseries.other_sources.imf import BuildData as BuildDataIMF
from lanka_data_timeseries.other_sources.world_bank import (
    BuildData as BuildDataWorldBank,
)

log = Log(__file__)
if __name__ == "__main__":
    for BuildData in [
        BuildDataADB,
        BuildDataWorldBank,
        BuildDataIMF,
    ]:
        log.info("Running " + BuildData.__name__)
        BuildData.build_data()
