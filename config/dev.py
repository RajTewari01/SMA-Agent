from .base import BaseConfig


class DevConfig(BaseConfig):
    DEBUG = True
    D_EXEC = True
    IMMEDIATE_EXEC = True
    IMMEDIATE_ERROR_VALIDATION = True
    CONFIG_TYPE = "dev"
