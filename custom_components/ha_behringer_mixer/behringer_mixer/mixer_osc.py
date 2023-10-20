import asyncio
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_server import AsyncIOOSCUDPServer


class OSCClientServer(AsyncIOOSCUDPServer):
    def __init__(self, address: str, dispatcher: Dispatcher, event_loop):
        super().__init__(("0.0.0.0", 0), dispatcher, event_loop)
        self.mixer_address = address
        self.event_loop = event_loop
        self.transport = None

    def send_message(self, address: str, vals):
        builder = OscMessageBuilder(address=address)
        vals = vals if vals is not None else []
        if not isinstance(vals, list):
            vals = [vals]
        for val in vals:
            builder.add_arg(val)
        msg = builder.build()
        self.transport.sendto(msg.dgram, self.mixer_address)

    def register_transport(self, transport):
        self.transport = transport
