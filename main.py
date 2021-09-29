from config_reader import ConfigReader

if __name__ == '__main__':
    config_reader = ConfigReader('data.json')
    config_reader.read_config()
