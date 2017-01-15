import datetime


class TravelTime:
    def __init__(self, timepoint: datetime.datetime, routes: dict):
        self.timepoint = timepoint
        self.routes = routes

    @classmethod
    def from_csv_row(cls, row: dict):
        timepoint = datetime.datetime.strptime(row['datetime'], '%Y%m%d %H:%M')
        routes = {key: value for key, value in row.items() if key != 'datetime'}
        return cls(timepoint, routes)
