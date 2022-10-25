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

    @property
    def db_path(self) -> Path:
        return self.user_data_dir / "db.db"

    def db_uri(self, read_only: bool = True) -> str:
        base_uri = f"sqlite+pysqlite:///{self.db_path.as_uri()}?uri=true"

        return base_uri + "&mode=ro" if read_only else base_uri

    election_url: str = "https://business.senedd.wales"

    @property
    def election_all_constituency_url(self) -> str:
        return f"{self.election_url}/mgElectionElectionAreaResults.aspx?Page=all&EID=18&RPID=1533467460"

    class Config:
        env_file = ".env"
        # https://github.com/samuelcolvin/pydantic/issues/1241
        keep_untouched = (cached_property,)


@cache
def get_settings():
    return Settings()
