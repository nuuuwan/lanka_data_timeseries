from lanka_data_timeseries.other_sources.world_bank import BuildData
from lanka_data_timeseries.other_sources.adb import BuildSummary

if __name__ == '__main__':
    BuildData.build_data()
    BuildSummary.build()
