import requests
import sys
from pytz import timezone
from datetime import datetime


def get_data_from_api(url, payload=None):
    response = requests.get(url, params=payload)
    if response.ok:
        return response.json()


def load_attempts(api_url):
    page = 1
    pages = 1
    while page <= pages:
        payload = {'page': page}
        page_data = get_data_from_api(api_url, payload)
        pages = page_data['number_of_pages']
        for record in page_data['records']:
            yield record
        page += 1


def get_midnighters(attempts):
    midnighters = set()
    for attempt in attempts:
        if is_midnighter(attempt):
            midnighters.add(attempt['username'])
    return midnighters


def is_midnighter(record):
    user_tz = timezone(record['timezone'])
    submit_time = datetime.fromtimestamp(
        record['timestamp'],
        tz=user_tz
    )
    midnight = 0
    morning = 6
    if morning >= submit_time.hour >= midnight:
        return True


if __name__ == '__main__':
    api_url = 'https://devman.org/api/challenges/solution_attempts/'
    attempts = load_attempts(api_url)
    try:
        midnighters = get_midnighters(attempts)
    except requests.exceptions.ConnectionError:
        sys.exit('Server is unavailable')

    print('Users who submit tasks at night:')
    for user in midnighters:
        print(user)
