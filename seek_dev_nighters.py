import requests
import sys
from pytz import timezone
from datetime import datetime, time


def get_json(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    return None


def load_attempts(api_url):
    pages = get_json(api_url)['number_of_pages']
    for page in range(1, pages+1):
        page_json = get_json(api_url + ('?page=%s' % page))
        for record in page_json['records']:
            yield record


def get_midnighters(attempts):
    midnighters = set()
    for record in attempts:
        if midnighter_check(record):
            midnighters.add(record['username'])
    return midnighters


def midnighter_check(record):
    user_tz = timezone(record['timezone'])
    submit_time = user_tz.localize(
        datetime.fromtimestamp(record['timestamp']),
        is_dst=None
    )
    midnight = user_tz.localize(
        datetime.combine(submit_time.date(), time(0, 0)),
        is_dst=None
    )
    morning = user_tz.localize(
        datetime.combine(submit_time.date(), time(6, 0)),
        is_dst=None
    )
    if morning >= submit_time >= midnight:
        return True


if __name__ == '__main__':
    api_url = 'https://devman.org/api/challenges/solution_attempts/'
    if not get_json(api_url):
        sys.exit('API url is unavailable')
    attempts = load_attempts(api_url)
    midnighters = get_midnighters(attempts)
    print('Users who submit tasks at night:')
    for user in midnighters:
        print(user)
