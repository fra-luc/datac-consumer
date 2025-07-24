import asyncio

import aiohttp

from downloaders.static_gtfs import StaticGTFSDownloader, StaticGTFSDownloaderSettings
from downloaders.vehicle_positions import (
    VehiclePositionsDownloader,
    VehiclePositionsDownloaderSettings,
)
from file_system.local import LocalFileSystem, LocalFileSystemSettings


async def consume():
    """
    datac consumer entrypoint:
        * consumes and downloads the real-time GTS feed
        * downloads static GTFS updates when available
    """
    async with aiohttp.ClientSession() as session:
        local_fs = LocalFileSystem(
            settings=LocalFileSystemSettings(),
        )
        static_gtfs_downloader = StaticGTFSDownloader(
            session=session, file_system=local_fs, settings=StaticGTFSDownloaderSettings()
        )
        vehicle_positions_downloader = VehiclePositionsDownloader(
            session=session,
            file_system=local_fs,
            settings=VehiclePositionsDownloaderSettings(),
        )
        await asyncio.gather(
            vehicle_positions_downloader.run(),
            static_gtfs_downloader.run(),
        )


def main():
    asyncio.run(consume())
