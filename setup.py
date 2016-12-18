import setuptools

setuptools.setup(
    name='ShowMeTheWayToGoHome',
    version='0.0a1',
    author='Jonatan Skogsfors',
    author_email='jonatan@skogsfors.net',
    packages=setuptools.find_packages(),
    license='MIT',
    package_data={
        'show_me_the_way_to_go_home': ['configuration.yml'],
    },
    entry_points={
        'console_scripts': [
            'update-traveltime-stats=show_me_the_way_to_go_home.update_traveltime_stats:main',
            'best-route-for-time=show_me_the_way_to_go_home.best_route_for_time:main',
        ],
    },
)
