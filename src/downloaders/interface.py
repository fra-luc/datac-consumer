import asyncio
from dataclasses import dataclass

import aiohttp
from pydantic_settings import BaseSettings

from file_system.interface import FileSystemInterface


class DownloaderSettings(BaseSettings):
    """
    Settings for Downloader istances
    """

    url: str
    """
    Real Time GTFS URL
    """
    frequency: int
    """
    Frequency of download in seconds
    """
    attempts: int
    """
    Number of download attempts before raising
    """
    retry_frequency: int
    """
    Frequency of download attempts in seconds
    """
    logging_level: str
    """
    Logging level
    """


@dataclass
class Downloader:
    session: aiohttp.ClientSession
    file_system: FileSystemInterface
    settings: DownloaderSettings

    async def _retry_download(self):
        attempt_num = 0
        while True:
            try:
                return await self._download()
            except aiohttp.ClientError as exc:
                attempt_num += 1
                await asyncio.sleep(self.settings.retry_frequency)
                if attempt_num == self.settings.attempts:
                    await self._on_download_failure(exc)
                    raise RuntimeError(f"Download failed after {self.settings.attempts} attempts") from exc

    async def _download(self):
        raise NotImplementedError

    async def _on_download_failure(self, exc: Exception):
        raise NotImplementedError

    async def run(self):
        """
        Starts downloading
        """
        raise NotImplementedError
