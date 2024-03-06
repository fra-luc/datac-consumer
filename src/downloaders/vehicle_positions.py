import asyncio
import logging
from dataclasses import dataclass

from pydantic_settings import SettingsConfigDict

from downloaders.helpers import configure_logger
from downloaders.interface import Downloader, DownloaderSettings


class VehiclePositionsDownloaderSettings(DownloaderSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="veh_positions_downloader_", extra="allow")


@dataclass
class VehiclePositionsDownloader(Downloader):
    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
        configure_logger(self.logger, logging.DEBUG)

    async def run(self):
        while True:
            message = await self._retry_download()
            self.file_system.save_real_time_gtfs_message(message)
            await asyncio.sleep(self.settings.frequency)

    async def _download(self):
        self.logger.debug("Downloading message...")
        async with self.session.get(self.settings.url) as response:
            return await response.content.read()

    async def _on_download_failure(self, exc: Exception):
        self.alerts.notify_feed_download_failure(exc)
