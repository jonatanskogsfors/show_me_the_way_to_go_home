"""Usage: update-taveltime-stats [options]

Options:
-h, --help                          Show this text.
-t <datetime>, --time=<datetime>    Optional datetime in the form YYYYmmddTHHMM

"""
import csv
import sys
from datetime import datetime

import docopt

from show_me_the_way_to_go_home.configuration import get_configuration
from show_me_the_way_to_go_home.time_math import next_five_minutes
from show_me_the_way_to_go_home.route_master import RouteMaster


def main():
    configuration = get_configuration()
    arguments = docopt.docopt(__doc__)

    if arguments['--time']:
        try:
            departure_time = datetime.strptime(arguments['--time'], "%Y%m%dT%H%M")
        except ValueError:
            print("'{}' is not a valid datetime. Exiting...".format(arguments['--time']))
            sys.exit(1)
    else:
        departure_time = datetime.now()

    departure_time = next_five_minutes(departure_time)

    route_master = RouteMaster(configuration.origin, configuration.destination)

    csv_row = {'datetime': departure_time.strftime("%Y%m%d %H:%M")}
    for route, waypoints in configuration.routes:
        csv_row[route] = route_master.duration_for_time_and_waypoint(departure_time, waypoints)

    _write_result_to_stats_file(configuration, csv_row)


def _write_result_to_stats_file(configuration, csv_row):
    _create_stats_file_if_needed(configuration)
    with configuration.stats_file.open('a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=configuration.csv_field_names)
        writer.writerow(csv_row)


def _create_stats_file_if_needed(configuration):
    if not configuration.stats_file.is_file():
        with configuration.stats_file.open('w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=configuration.csv_field_names)
            writer.writeheader()


if __name__ == '__main__':
    main()
