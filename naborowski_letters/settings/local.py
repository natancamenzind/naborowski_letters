from .base import *


DATABASES = {
    'default': {
        **env.db('DATABASE_URL'),
        'CONN_MAX_AGE': 600,  # 10m
    },
}
