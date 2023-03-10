config = {
    'version': 1,
    'formatters': {
        'simpleFormatter': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simpleFormatter',
            'stream': 'ext://sys.stdout'
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'simpleFormatter',
            'filename': 'logs/log.log',
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'Finder': {
            'handlers': ['consoleHandler', 'fileHandler'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['consoleHandler', 'fileHandler']
    }
}