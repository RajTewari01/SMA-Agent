from .base import BaseConfig


class ProdConfig(BaseConfig):
    DEBUG = False
    # LLM_MODELS = paths(mnt/models)
    IMMEDIATE_EXEC = False
    IMMEDIATE_ERROR_VALIDATION = False
    IMMEDIATE_EXEC = False
    CONFIG_TYPE = "prod"
