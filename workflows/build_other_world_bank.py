from lanka_data_timeseries.BuildSummary import BuildSummary
from lanka_data_timeseries.other_sources.world_bank import BuildData

if __name__ == '__main__':
    BuildData.build_data()
    BuildSummary.build()
