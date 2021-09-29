from const import ConfigNames

import json
import sys


class InterfaceData(object):
    """
    Data class storing information on an interface
    """
    def __init__(self, name='', description='', max_frame_size=None, config=None, port_channel_id=None):
        self.name = name
        self.description = description
        self.max_frame_size = max_frame_size
        self.config = config
        self.port_channel = port_channel_id

    def __str__(self):
        return 'Name: {}, description: {}, max_frame_size: {}, config: {}, port_channel_id: {}' \
            .format(self.name, self.description, self.max_frame_size, self.config, self.port_channel)


class ConfigReader(object):
    """
    Class responsible for reading config file
    """
    def __init__(self, file_path):
        try:
            config_file = open(file_path, 'r')
        except OSError as e:
            print('Exception occured while opening file {}'.format(e.filename))
            print(e.args)
            sys.exit(1)
        self._config_dict = json.load(config_file)[ConfigNames.ROOT_FRINX_CONFIGURATION]
        self._interfaces = {}
        self._port_channel_interfaces = {}

    def read_config(self):
        """
        Public endpoint of ConfigReader
        returns dictionaries of InterfaceData
        """
        self._read_from_cisco_native()
        self._read_from_openconfig_interfaces()
        return self._port_channel_interfaces, self._interfaces

    def _read_from_cisco_native(self):
        """
        Reads the section of config file 'Cisco-IOS-XE-native:native'
        Calls  _read_interface_data_cisco to store actual data
        """
        cisco_config = self._config_dict[ConfigNames.CISCO_NATIVE][ConfigNames.SECTION_INTERFACE]

        # Read port channel data
        # Port Channels have to go first so we can reference them in GigabitEthernet interfaces
        port_channels = cisco_config.get(ConfigNames.SECTION_INTERFACE_PORT_CHANNEL, [])
        for port_channel in port_channels:
            self._read_interface_data_cisco(ConfigNames.GROUP_PORT_CHANNEL, port_channel)

        # Read The rest
        # For implementation storing Loopback and BDI interfaces, simply add GROUP to the list below
        for interface_group in (ConfigNames.GROUP_GIGABIT_ETH, ConfigNames.GROUP_TEN_GIGABIT_ETH):
            interfaces_data = cisco_config.get(interface_group, [])
            for interface_data in interfaces_data:
                self._read_interface_data_cisco(interface_group, interface_data)

    def _read_interface_data_cisco(self, interface_group, interface_data):
        """
        Gets interface group (port-channel, TenGigabitEthernet etc.) and interface data dictionary and
        Create data class for the interface and store it in dictionary - interfaces or port_channel_interfaces
        """
        name = interface_data.get(ConfigNames.DATA_NAME, '')
        full_name = interface_group + str(name)
        description = interface_data.get(ConfigNames.DATA_DESCRIPTION, '')
        max_frame_size = interface_data.get(ConfigNames.DATA_MAX_FRAME_SIZE, None)

        # port_channel is a reference to an interface of group Port-channel
        port_channel_data = interface_data.get(ConfigNames.DATA_PORT_CHANNEL, None)
        port_channel = None
        if port_channel_data:
            port_channel_number = port_channel_data.get(ConfigNames.DATA_PORT_CHANNEL_NUMBER, None)
            port_channel = self._port_channel_interfaces['Port-channel{}'.format(port_channel_number)]

        # Create object
        interface_data_object = InterfaceData(name=full_name,
                                              description=description,
                                              max_frame_size=max_frame_size,
                                              port_channel_id=port_channel)
        if interface_group == ConfigNames.GROUP_PORT_CHANNEL:
            self._port_channel_interfaces[full_name] = interface_data_object
        else:
            self._interfaces[full_name] = interface_data_object

    def _read_from_openconfig_interfaces(self):
        """
        Reads the section of config file 'openconfig-interfaces:interfaces'
        We assert that proper data objects were created during reading of CISCO section
        We only need to add configuration of interfaces here
        """
        openconfig = self._config_dict[ConfigNames.OPEN_CONFIG_INTERFACES][ConfigNames.SECTION_INTERFACE]
        for interface_data in openconfig:
            name = interface_data.get(ConfigNames.DATA_NAME, '')
            if name in self._interfaces.keys():
                config_dict = interface_data.get(ConfigNames.DATA_CONFIG, None)
                self._interfaces[name].config = config_dict
            elif name in self._port_channel_interfaces.keys():
                config_dict = interface_data.get(ConfigNames.DATA_CONFIG, None)
                self._port_channel_interfaces[name].config = config_dict
