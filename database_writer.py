from const import ConfigNames

import psycopg2
import json


class DatabaseWriter(object):
    """
    Class that connects to a database and writes
    """
    def __init__(self):
        self.conn = psycopg2.connect(ConfigNames.DB_CONN_STRING)
        self.cursor = self.conn.cursor()

    def write_interface(self, interface_data):
        """
        Writes data on interface into database. If an interface has port channel specified, get the port channel ID
        from DB first
        """
        port_channel_id = None
        if interface_data.port_channel:
            port_channel_name = interface_data.port_channel.name
            sql = "SELECT id FROM interfaces WHERE name = %s"
            self.cursor.execute(sql, (port_channel_name, ))
            if self.cursor.rowcount == 1:
                port_channel_id = self.cursor.fetchone()[0]

        sql = ("INSERT INTO interfaces(name, description, max_frame_size, config, port_channel_id) "
               "VALUES(%s, %s, %s, %s, %s)")
        self.cursor.execute(sql, (interface_data.name,
                                  interface_data.description,
                                  interface_data.max_frame_size,
                                  json.dumps(interface_data.config),
                                  port_channel_id
                                  )
                            )
        self.conn.commit()

    def finalize(self):
        """
        Close the DB connection
        """
        self.cursor.close()
        self.conn.close()
