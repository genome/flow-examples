from setuptools import setup

entry_points = '''
[flow.commands]
hello-world = flow_hello_world.command:HelloWorld
'''

setup(
        name = 'flow_hello_world',
        version = '0.1',
        packages = ['flow_hello_world'],
        entry_points = entry_points,
        install_requires = [
            'flow',
        ],
)
