from flow.commands.base import CommandBase
from flow.configuration.inject.broker import BrokerConfiguration
from flow.configuration.inject.redis_conf import RedisConfiguration
from flow.configuration.inject.service_locator import ServiceLocatorConfiguration
from flow.petri_net.builder import Builder
from flow.service_locator import ServiceLocator

import flow_hello_world.future_net
import flow.interfaces
import injector
import redis


@injector.inject(storage=flow.interfaces.IStorage,
        service_locator=ServiceLocator)
class HelloWorld(CommandBase):
    injector_modules = [
            BrokerConfiguration,
            RedisConfiguration,
            ServiceLocatorConfiguration,
    ]

    @staticmethod
    def annotate_parser(parser):
        pass

    def setup_net(self):
        # Gather all the information about the net locally.
        future_net = flow_hello_world.future_net.HelloWorldFutureNet()

        builder = Builder(self.storage)

        # Save the actual Petri net representation to Redis
        self.net = builder.store(future_net, variables={}, constants={})

        # Return the index of the start place
        return builder.future_places[future_net.start_place]

    def _execute(self, parsed_arguments):
        start_place_index = self.setup_net()

        color_group = self.net.add_color_group(1)
        color = color_group.begin  # The first color in the color group.

        return self.service_locator['orchestrator'].create_token(self.net.key,
                start_place_index, color, color_group.idx)
