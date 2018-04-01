import configparser

def check_config(file_name):
    try:
        open(file_name)
    except IOError:
        print('NOTE: Config file was not found.')
        return False
    return True

def create_config_template():
    config = configparser.ConfigParser()
    config['Proxies'] = {'https': 'https://IP:PORT',
                         'http': 'http://111.111.111.111:1111'}
    config['Storage'] = {'fileName': 'storage.txt',
                         'filePath': 'path'}
    config['SpotifyApp'] = {'client_id': 'Your client id',
                         'client_secret': 'Your client secret id',
                         'redirect_uri': 'http://localhost'}
    config['Spotify'] = {'username': 'Your Spotify username',
                         'scope': 'user-library-read'}
    config['Youtube'] = {'maxDuration': '4'}
    with open('config.ini', 'w') as configfile:
      config.write(configfile)

def read_config_section(section):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[section]