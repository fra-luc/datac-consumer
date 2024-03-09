from dataclasses import dataclass


@dataclass
class AlertsInterface:
    async def notify_real_time_feed_download_failure(self, exc: Exception):
        """
        Notifies download failures of the real time GTFS feed
        """
        raise NotImplementedError

    async def notify_static_gtfs_download_failure(self, exc: Exception):
        """
        Notifies download failures of the real time GTFS feed
        """
        raise NotImplementedError

    async def notify_file_system_almost_full(self, free_space: int):
        """
        Notifies that file system space is almost full
        """
        raise NotImplementedError
