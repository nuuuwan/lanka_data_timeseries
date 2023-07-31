import os
import tempfile

from utils_future import WWWFuture

DIR_TMP_DATA = os.path.join(
    tempfile.gettempdir(),
    'tmp.lanka_data_timeseries',
)

URL_CBSL = 'https://www.cbsl.lk'
URL_ERESEARCH = WWWFuture.join(URL_CBSL, 'eresearch')
N_SUBJECTS = 35
MONTHS = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]
QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']

HALVES = ['H1', 'H2']

DEFAULT_SCALE = ''
DEFAULT_FREQUENCY_NAME = 'Annual'
DEFAULT_I_SUBJECT = -1
DEFAULT_UNIT = ''
DEFAULT_FOOTNOTES = {}
