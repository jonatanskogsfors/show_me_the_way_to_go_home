import datetime
import statistics
from typing import Tuple, List

from show_me_the_way_to_go_home import time_math
from show_me_the_way_to_go_home.models.travel_time import TravelTime


class Weekday:
    def __init__(self, weekday: int, traveltimes: List[TravelTime]):
        self._weekday = weekday
        timepoints_for_weekday = self._timepoints_for_weekday(traveltimes)
        self._timepoints = timepoints_for_weekday

    def median_travel_time_for_timepoint_and_route(self, timepoint: datetime.time, route: str) -> int:
        median_travel_times = self.median_travel_time_for_timepoint(timepoint)
        return median_travel_times[route]

    def median_travel_time_for_timepoint(self, timepoint: datetime.time) -> dict:
        timepoint = time_math.next_five_minutes(timepoint)
        routes = self._timepoints[timepoint]
        median_travel_times = {route: statistics.median(travel_times) for route, travel_times in routes.items()}
        return median_travel_times

    def best_route_for_timepoint(self, timepoint: datetime.time) -> Tuple[List[str], int]:
        median_travel_times = self.median_travel_time_for_timepoint(timepoint)
        shortest_travel_time = None
        fastest_routes = []
        for route, travel_time in median_travel_times.items():
            if travel_time < shortest_travel_time or shortest_travel_time is None:
                shortest_travel_time = travel_time
                fastest_routes = [route]
            elif travel_time == shortest_travel_time:
                fastest_routes.append(route)
        return fastest_routes, shortest_travel_time

    def median_travel_times_for_route(self, route: str) -> Tuple[Tuple[datetime.time, int]]:
        median_travel_times = [(timepoint, statistics.median(routes[route]))
                               for timepoint, routes in self._timepoints.items()]
        median_travel_times.sort()
        return tuple(median_travel_times)

    def _timepoints_for_weekday(self, traveltimes: List[TravelTime]):
        traveltimes_for_weekday = [traveltime for traveltime in traveltimes
                                   if traveltime.timepoint.weekday() == self._weekday]

        timepoint_for_weekday = {}
        for traveltime in traveltimes_for_weekday:
            if traveltime.timepoint.time not in timepoint_for_weekday:
                timepoint_for_weekday[traveltime.timepoint.time()] = {route: [] for route in traveltime.routes.keys()}
            for route, travel_time in traveltime.routes.items():
                timepoint_for_weekday[traveltime.timepoint.time()][route].append(travel_time)
        return timepoint_for_weekday


# Hur lång tid tar det att åka hem klockan x?
# Ge mig ett diagram för dagen.

