import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime

from pydantic_settings import SettingsConfigDict

from downloaders.helpers import configure_logger
from downloaders.interface import Downloader, DownloaderSettings


class StaticGTFSDownloaderSettings(DownloaderSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="static_gtfs_downloader_", extra="allow")


@dataclass
class StaticGTFSDownloader(Downloader):
    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        configure_logger(self.logger, self.settings.logging_level)

    async def run(self):
        last_downloaded = None

        while True:
            last_modified = await self._get_last_modified_static_gtfs_timestamp()
            if not last_downloaded or last_modified > last_downloaded:
                self.logger.debug("Found new static GTFS update...")
                content = await self._retry_download()
                await self.file_system.save_static_gtfs_data(content, last_modified)
                self.logger.debug("Saved new static GTFS update!")
                last_downloaded = last_modified
            await asyncio.sleep(self.settings.frequency)

    async def _get_last_modified_static_gtfs_timestamp(self) -> datetime:
        async with self.session.head(self.settings.url) as response:
            return datetime.strptime(response.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")

    async def _download(self):
        self.logger.debug("Downloading static GTFS update...")
        async with self.session.get(self.settings.url) as response:
            return await response.content.read()

    async def _on_download_failure(self, exc: Exception):
        self.logger.error("Static GTFS update download failed!")
        await self.alerts.notify_static_gtfs_download_failure(exc)
