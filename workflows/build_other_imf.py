from lanka_data_timeseries.other_sources.imf import BuildData
from lanka_data_timeseries.BuildSummary import BuildSummary

if __name__ == '__main__':
    BuildData.build_data()
    BuildSummary.build()
