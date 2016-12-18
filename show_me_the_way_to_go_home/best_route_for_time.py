"""Usage: best-route [options] [<time>]

Options:
-h, --help                          Show this text.
"""
import csv
import datetime
import sys

import docopt
from collections import defaultdict

from show_me_the_way_to_go_home.configuration import get_configuration
from show_me_the_way_to_go_home.math import next_five_minutes


def main():
    configuration = get_configuration()
    arguments = docopt.docopt(__doc__)

    now = datetime.datetime.now()
    if arguments['<time>']:
        hour, minute = arguments['<time>'].split(':')
        departure_time = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
    else:
        departure_time = now

    departure_time = next_five_minutes(departure_time)

    traveltime_stats = load_traveltime_stats(configuration)

    for starttime, routes in traveltime_stats[departure_time.weekday()].items():
        print(starttime)
        for route, times in routes.items():
            print("{}: {}".format(route, times))



def load_traveltime_stats(configuration):
    if not configuration.stats_file.is_file():
        print("Could not find stats file at '{}'".format(configuration.stats_file))
        sys.exit(1)

    traveltime_stats = {i: defaultdict(lambda: defaultdict(list)) for i in range(7)}

    with configuration.stats_file.open('r') as stats_file:
        reader = csv.DictReader(stats_file)
        routes = reader.fieldnames[1:]
        for row in reader:
            time = datetime.datetime.strptime(row['datetime'], '%Y%m%d %H:%M')
            hour_minute = time.strftime('%H:%M')
            weekday = time.weekday()
            for route in routes:
                traveltime_stats[weekday][hour_minute][route].append(row[route])
    return traveltime_stats

if __name__ == '__main__':
    main()
