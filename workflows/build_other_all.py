from lanka_data_timeseries.BuildSummary import BuildSummary
from lanka_data_timeseries.other_sources import adb, imf, misc, world_bank

if __name__ == '__main__':
    for module in [adb, imf, world_bank, misc]:
        module.BuildData.build_data()
    BuildSummary.build()
