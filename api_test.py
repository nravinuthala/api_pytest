import requests
import json
import pytest
from datetime import datetime, date

def api_call(dob, unit):
    """
    This method makes the API call by accepting the required parameters. This will be invoked by the test method 
    by passing the test data as parameters.
    From the response, the text is extracted and converted to Python dictionary using json loads method and 
    then the required attribute is extracted for comparison and assertion.
    """
    url = f"https://lx8ssktxx9.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?dateofbirth={dob}&unit={unit}"
    response = requests.get(url)
    response_msg = json.loads(response.text)
    return response_msg['message']

api_call('1900-01-01', 'months')

def date_diff_util():
    """
    Since the expected result keeps changing daily, this method calculates the date when the test case is written 
    and the date when it is being executed and accordingly adjusts the expected result, so that test case does not 
    fail for date change reasons.
    """
    test_written_date_str = "2023-08-10"
    test_written_date = datetime.strptime(test_written_date_str, '%Y-%m-%d').date()
    current_date = datetime.date(datetime.today())
    diff_days = (current_date - test_written_date).days
    diff_hours = diff_days * 24
    diff_weeks = diff_days // 7
    diff_months = diff_days // 30
    return diff_months, diff_days, diff_hours, diff_weeks

diff_months, diff_days, diff_hours, diff_weeks = date_diff_util()

@pytest.mark.parametrize("dob,unit,expected", [
    ('1900-01-01', 'hour', f'{3456 - diff_hours} hours left'),
    ('1900-01-01', 'day', f'{144 - diff_days} days left'),
    ('1900-01-01', 'week', f'{20 - diff_weeks} weeks left'),
    ('1900-01-01', 'month', f'{4 - diff_months} months left'),
    ('1900-01-01', 'months', None),
    ('1900-01-00', 'month', 'Please specify dateofbirth in ISO format YYYY-MM-DD'),
])
def test_api_call(dob, unit, expected):
    assert api_call(dob, unit) == expected
    