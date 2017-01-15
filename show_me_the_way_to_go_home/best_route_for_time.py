"""Usage: best-route [options] [<time>]

Options:
-h, --help                          Show this text.
"""
import csv
import datetime
import sys

import docopt
from typing import Dict

from show_me_the_way_to_go_home.configuration import get_configuration
from show_me_the_way_to_go_home.models.travel_time import TravelTime
from show_me_the_way_to_go_home.models.weekday import Weekday
from show_me_the_way_to_go_home.time_math import next_five_minutes


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

    print(traveltime_stats[now.weekday()].median_travel_times_for_route('via_alvsborgsbron'))



def load_traveltime_stats(configuration) -> Dict[int, Weekday]:
    if not configuration.stats_file.is_file():
        print("Could not find stats file at '{}'".format(configuration.stats_file))
        sys.exit(1)

    traveltimes = []
    with configuration.stats_file.open('r') as stats_file:
        reader = csv.DictReader(stats_file)
        for row in reader:
            traveltimes.append(TravelTime.from_csv_row(row))

    traveltime_stats = {i: Weekday(i, traveltimes) for i in range(7)}
    return traveltime_stats


if __name__ == '__main__':
    main()



