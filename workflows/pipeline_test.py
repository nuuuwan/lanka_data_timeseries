from utils import Log

from lanka_data_timeseries.cbsl import FREQUENCY_LIST, Config
from workflows.pipeline import inner_unsafe

log = Log(__name__)


def main():
    config = Config(FREQUENCY_LIST[0], 7)
    if not inner_unsafe(config):
        raise Exception('pipieline_test FAILED!')


if __name__ == '__main__':
    main()
