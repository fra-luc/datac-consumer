import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime

from pydantic_settings import SettingsConfigDict

from downloaders.helpers import configure_logger
from downloaders.interface import Downloader, DownloaderSettings

logger = logging.getLogger(__name__)
configure_logger(logger, logging.DEBUG)


class StaticGTFSDownloaderSettings(DownloaderSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="static_gtfs_downloader_", extra="allow")


@dataclass
class StaticGTFSDownloader(Downloader):
    async def run(self):
        last_downloaded = None

        while True:
            last_modified = await self._get_last_modified_schedule_timestamp()
            if not last_downloaded or last_modified > self.last_downloaded:
                content = await self._retry_download()
                self.file_system.save_static_gtfs_data(content, last_modified)
                self.last_downloaded = last_modified
            await asyncio.sleep(self.settings.frequency)

    async def _get_last_modified_schedule_timestamp(self) -> datetime:
        async with self.session.head(self.settings.url) as response:
            return datetime.strptime(response.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")

    async def _download(self):
        logger.info("Downloading schedule update...")
        async with self.session.get(self.settings.url) as response:
            return await response.content.read()
