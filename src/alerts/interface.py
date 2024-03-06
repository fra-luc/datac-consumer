from dataclasses import dataclass


@dataclass
class AlertsInterface:
    def notify_feed_download_failure(self, exc: Exception):
        """
        Notifies download failures of the real time GTFS feed
        """
        raise NotImplementedError

    def notify_save_failure(self, exc: Exception):
        """
        Notifies save failures of the downloaded data
        """
        raise NotImplementedError
