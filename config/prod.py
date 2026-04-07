
from .base import BaseConfig


class ProdConfig(BaseConfig):
    DEBUG = False
    # LLM_MODELS = paths(mnt/models)
    IMMEDIATE_EXEC = False
