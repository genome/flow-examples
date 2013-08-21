from flow.shell_command.petri_net import actions
from flow.shell_command.petri_net import future_nets


class ShellOWorldFutureNet(future_nets.ShellCommandNet):
    def __init__(self):
        future_nets.ShellCommandNet.__init__(self, name='shell-o-world net',
                dispatch_action_class=actions.ForkDispatchAction,
                command_line=['touch', 'lol_it_worked.txt'])

        self.wrap_with_places()
