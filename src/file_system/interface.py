from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileSystemInterface:
    async def save_real_time_gtfs_message(self, message: bytes):
        """
        Save a real-time GTFS message content in the file system
        """
        raise NotImplementedError

    async def save_static_gtfs_data(self, content: bytes, last_modified: datetime):
        """
        Save a static GTFS file content in the file system
        """
        raise NotImplementedError

    async def is_almost_full(self):
        """
        Checks whether the file system is almost full
        """
        raise NotImplementedError
