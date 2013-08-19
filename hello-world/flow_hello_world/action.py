from flow.petri_net.actions.base import BasicActionBase
from twisted.internet import defer


class HelloWorldAction(BasicActionBase):
    required_arguments = ['text']

    def execute(self, net, color_descriptor, active_tokens, service_interfaces):
        # The work we are doing is to simply log that we got here.
        print '\n\n\nHello: %s\n\n' % self.args['text']

        # The map passes the tokens we received along to our output places.
        return map(net.token, active_tokens), defer.succeed(None)
