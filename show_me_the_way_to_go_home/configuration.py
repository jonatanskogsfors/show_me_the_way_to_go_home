import pathlib

import yaml

from show_me_the_way_to_go_home import configuration_path


class Configuration:
    def __init__(self, config_path):
        config_path = pathlib.Path(config_path)
        with config_path.open('r') as config_file:
            self._config = yaml.load(config_file.read())

    @property
    def origin(self):
        return self._config.get('origin')

    @property
    def destination(self):
        return self._config.get('destination')

    @property
    def api_key(self):
        return self._config.get('api_key')

    @property
    def routes(self):
        return self._config.get('routes').items()

    @property
    def stats_file(self):
        return pathlib.Path(self._config.get('stats_file'))

    @property
    def csv_field_names(self):
        routes = self._config.get('routes', [])
        return tuple(['datetime'] + sorted(routes))


def get_configuration():
    return Configuration(configuration_path)
