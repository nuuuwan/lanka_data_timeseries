from utils import Time, TimeFormat

from cbsl.edl.Frequency import Frequency


def get_next_year():
    return int(TimeFormat('%Y').stringify(Time.now())) + 1


END_YEAR = get_next_year()
START_YEAR = END_YEAR - 60

FREQUENCY_LIST = [
    Frequency(
        'Annual',
        'A',
        {
            'ContentPlaceHolder1_txtYearFrom': START_YEAR,
            'ContentPlaceHolder1_txtYearTo': END_YEAR,
        },
    ),
    Frequency(
        'Census Year',
        'C',
        {
            'ContentPlaceHolder1_txtCensusYearFrom': START_YEAR,
            'ContentPlaceHolder1_txtCensusYearTo': END_YEAR,
        },
    ),
    Frequency(
        'Academic Year',
        'E',
        {
            'ContentPlaceHolder1_txtAcedemicYearFrom': START_YEAR,
            'ContentPlaceHolder1_txtAcedemicYearTo': END_YEAR,
        },
    ),
    Frequency(
        'Half Yearly',
        'H',
        {
            'ContentPlaceHolder1_txtHalfFrom': START_YEAR,
            'ContentPlaceHolder1_txtHalfTo': END_YEAR,
        },
    ),
    Frequency(
        'Quarterly',
        'Q',
        {
            'ContentPlaceHolder1_txtYearQuarterlyFrom': START_YEAR,
            'ContentPlaceHolder1_txtYearQuarterlyTo': END_YEAR,
        },
    ),
    Frequency(
        'Monthly',
        'M',
        {
            'ContentPlaceHolder1_txtYearMonthly1': f'{START_YEAR}-01',
            'ContentPlaceHolder1_txtYearMonthly2': f'{END_YEAR}-01',
        },
    ),
    Frequency(
        'Daily',
        'D',
        {
            'ContentPlaceHolder1_txtDateFrom': f'{START_YEAR}-01-01',
            'ContentPlaceHolder1_txtDateTo': f'{END_YEAR}-01-01',
        },
    ),
    Frequency('On-Availablity', 'O', {}),
]
