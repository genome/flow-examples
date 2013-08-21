from setuptools import setup

entry_points = '''
[flow.commands]
shell-o-world = flow_shell_o_world.command:ShellOWorld
'''

setup(
        name = 'flow_shell_o_world',
        version = '0.1',
        packages = ['flow_shell_o_world'],
        entry_points = entry_points,
        install_requires = [
            'flow',
        ],
)
