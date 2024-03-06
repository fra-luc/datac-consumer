from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from alerts.interface import AlertsInterface

from .interface import FileSystemInterface


class LocalFileSystemSettings(BaseSettings):
    real_time_gtfs_download_path: Path
    """
    Path where to download the real time GTFS messages
    """
    static_gtfs_download_path: Path
    """
    Path where to download the static GTFS updates
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="local_", extra="allow")


@dataclass
class LocalFileSystem(FileSystemInterface):
    settings: LocalFileSystemSettings
    alerts: AlertsInterface

    def __post_init__(self):
        self.settings.real_time_gtfs_download_path.mkdir(parents=True, exist_ok=True)
        self.settings.static_gtfs_download_path.mkdir(parents=True, exist_ok=True)

    def save_real_time_gtfs_message(self, message: bytes):
        now = datetime.utcnow().isoformat(timespec="seconds")

        with open(self.settings.real_time_gtfs_download_path / f"{now}.binpb", "wb") as f:  # TODO retry and alerts
            f.write(message)

    def save_static_gtfs_data(self, content: bytes, last_modified: datetime):
        fname = last_modified.isoformat()

        with open(self.settings.static_gtfs_download_path / f"{fname}.zip", "wb") as f:  # TODO retry and alerts
            f.write(content)

    def is_file_system_almost_full(self):
        raise NotImplementedError
