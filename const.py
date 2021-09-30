class ConfigNames(object):
    # root config sections
    ROOT_FRINX_CONFIGURATION = 'frinx-uniconfig-topology:configuration'
    CISCO_NATIVE = 'Cisco-IOS-XE-native:native'
    IETF_INTERFACES = 'ietf-interfaces:interfaces'
    OPEN_CONFIG_INTERFACES = 'openconfig-interfaces:interfaces'

    # Sections of CISCO config section
    SECTION_INTERFACE = 'interface'
    SECTION_INTERFACE_BDI = 'BDI'
    SECTION_INTERFACE_LOOPBACK = 'Loopback'
    SECTION_INTERFACE_PORT_CHANNEL = 'Port-channel'
    SECTION_INTERFACE_TEN_GIGABIT_ETH = 'TenGigabitEthernet'
    SECTION_INTERFACE_GIGABIT_ETH = 'GigabitEthernet'

    # Data items
    DATA_NAME = 'name'
    DATA_DESCRIPTION = 'description'
    DATA_PORT_CHANNEL = 'Cisco-IOS-XE-ethernet:channel-group'
    DATA_PORT_CHANNEL_NUMBER = 'number'
    DATA_CONFIG = 'config'
    DATA_MAX_FRAME_SIZE = 'mtu'

    # interface group names
    GROUP_PORT_CHANNEL = 'Port-channel'
    GROUP_LOOPBACK = 'Loopback'
    GROUP_BDI = 'BDI'
    GROUP_TEN_GIGABIT_ETH = 'TenGigabitEthernet'
    GROUP_GIGABIT_ETH = 'GigabitEthernet'

    # DB CONN STRING
    DB_CONN_STRING = 'dbname=testdb user=postgres password=*******'
