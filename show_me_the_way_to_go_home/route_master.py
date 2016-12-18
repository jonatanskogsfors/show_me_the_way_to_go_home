import googlemaps

API_KEY = 'AIzaSyAWGBIpY1_G8siFlvCPqGi4KAStP4nNymY'

class RouteMasterError(Exception):
    pass

class RouteMaster:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.client = googlemaps.Client(key=API_KEY)

    def duration_for_time_and_waypoint(self, departure_time, waypoint):
        directions_result = self.client.directions(
            origin=self.origin,
            destination=self.destination,
            waypoints=waypoint,
            mode='driving',
            departure_time=departure_time,
            alternatives=False)

        route = directions_result.pop()
        number_of_legs = len(route['legs'])
        if number_of_legs != 1:
            raise RouteMasterError(
                "Route was expected to have exactly one leg but had {} legs.".format(number_of_legs))

        leg = route['legs'].pop()
        duration_in_minutes = round(leg['duration_in_traffic']['value'] / 60)
        return duration_in_minutes
