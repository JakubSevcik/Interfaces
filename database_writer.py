from const import ConfigNames


class DatabaseWriter(object):
    def __init__(self, port_channel_interfaces, interfaces):
        self.port_channel_interfaces = port_channel_interfaces
        self.interfaces = interfaces
