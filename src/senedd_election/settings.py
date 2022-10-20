from functools import cache, cached_property
from os import makedirs
from pathlib import Path

from appdirs import user_data_dir
from pydantic import BaseSettings

from .utils import package


class Settings(BaseSettings):
    log_level: str = "ERROR"

    @cached_property
    def user_data_dir(self) -> Path:
        dir = user_data_dir(appname=package())
        makedirs(dir, exist_ok=True)
        return Path(dir)

    class Config:
        env_file = ".env"
        # https://github.com/samuelcolvin/pydantic/issues/1241
        keep_untouched = (cached_property,)


@cache
def get_settings():
    return Settings()
