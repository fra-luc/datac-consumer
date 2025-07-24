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
        configure_logger(self.logger, self.settings.logging_level)

    async def run(self):
        while True:
            message = await self._retry_download()
            await self.file_system.save_real_time_gtfs_message(message)
            if await self.file_system.is_almost_full():
                self.logger.warning("File system is almost full!")
            self.logger.debug("Saved feed message!")
            await asyncio.sleep(self.settings.frequency)

    async def _download(self):
        self.logger.debug("Downloading feed message...")
        async with self.session.get(self.settings.url) as response:
            return await response.content.read()

    async def _on_download_failure(self, exc: Exception):
        self.logger.error("Failed to download feed message!")
