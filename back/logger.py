import os
import logging
import logging.config


def get_logger(root: str, debug: bool) -> logging.Logger:
    """Setup root logger"""
    min_log_level = 'DEBUG' if debug else 'INFO'

    log_root = os.path.join(root, 'log')
    file_name = os.path.join(log_root, 'messages.log')

    if not os.path.exists(log_root):
        os.mkdir(log_root)

    config = {
        'version': 1,
        'formatters': {
            'short': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s :: %(levelname)s > %(message)s',
            },
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s :: <%(filename)s:%(lineno)s - %(funcName)s()>  %(levelname)s > %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': min_log_level,
                'formatter': 'short'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 10240000,
                'backupCount': 5,
                'filename': file_name,
                'formatter': 'detailed',
            },
        },
        'root': {
            'level': min_log_level,
            'handlers': ['console', 'file']
        },
    }

    logging.config.dictConfig(config)
    return logging.root
