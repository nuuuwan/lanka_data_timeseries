from lanka_data_timeseries.other_sources.misc.multi_data import \
    BuildData as BuildDataMulti
from lanka_data_timeseries.other_sources.misc.single_data import \
    BuildData as BuildDataSingle
from lanka_data_timeseries.other_sources.adb import BuildSummary

if __name__ == '__main__':
    BuildDataMulti.build_data()
    BuildDataSingle.build_data()
    BuildSummary.build()
