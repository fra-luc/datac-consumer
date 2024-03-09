import asyncio

import aiohttp

from alerts.mail_gun import MailGunAlerts, MailGunSettings
from downloaders.static_gtfs import StaticGTFSDownloader, StaticGTFSDownloaderSettings
from downloaders.vehicle_positions import (
    VehiclePositionsDownloader,
    VehiclePositionsDownloaderSettings,
)
from file_system.local import LocalFileSystem, LocalFileSystemSettings


async def main():
    """
    datac consumer entrypoint:
        * consumes and downloads the real-time GTS feed
        * downloads static GTFS updates when available
    """
    async with aiohttp.ClientSession() as session:
        mail_gun_alerts = MailGunAlerts(settings=MailGunSettings())
        local_fs = LocalFileSystem(
            settings=LocalFileSystemSettings(),
            alerts=mail_gun_alerts,
        )
        static_gtfs_downloader = StaticGTFSDownloader(
            session=session, alerts=mail_gun_alerts, file_system=local_fs, settings=StaticGTFSDownloaderSettings()
        )
        vehicle_positions_downloader = VehiclePositionsDownloader(
            session=session,
            alerts=mail_gun_alerts,
            file_system=local_fs,
            settings=VehiclePositionsDownloaderSettings(),
        )
        await asyncio.gather(
            vehicle_positions_downloader.run(),
            static_gtfs_downloader.run(),
        )


if __name__ == "__main__":
    asyncio.run(main())
