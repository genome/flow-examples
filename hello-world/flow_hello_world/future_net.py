from flow.petri_net import future
from flow_hello_world.action import HelloWorldAction


class HelloWorldFutureNet(future.FutureNet):
    def __init__(self):
        future.FutureNet.__init__(self)

        self.start_place = self.add_place(name='start')
        self.stop_place = self.add_place(name='stop')

        self.transition = self.bridge_places(self.start_place, self.stop_place,
                name='hello-world transition')
        self.transition.action = future.FutureAction(cls=HelloWorldAction,
                text='World')
