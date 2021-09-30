from config_reader import ConfigReader
from database_writer import DatabaseWriter

if __name__ == '__main__':
    # init classes
    config_reader = ConfigReader('configClear_v2.json')
    database_writer = DatabaseWriter()

    # Get the interfaces from config
    port_channel_interfaces, interfaces = config_reader.read_config()

    # First write port channel interfaces, so we can reference them later
    for interface in port_channel_interfaces:
        database_writer.write_interface(interface)

    # now write the rest
    for interface in interfaces:
        database_writer.write_interface(interface)

    # close DB connection
    database_writer.finalize()
