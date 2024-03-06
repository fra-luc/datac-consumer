from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileSystemInterface:
    def save_real_time_gtfs_message(self, message: bytes):
        raise NotImplementedError

    def save_static_gtfs_data(self, content: bytes, last_modified: datetime):
        raise NotImplementedError

    def is_file_system_almost_full(self):
        raise NotImplementedError
