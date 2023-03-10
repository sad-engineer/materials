from service.logger_settings import config

config['loggers'] = {
    'Finder': {
        'handlers': ['consoleHandler', 'fileHandler'],
        'level': 'INFO',
        'propagate': False
    }
}
