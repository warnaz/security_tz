from datetime import datetime, timezone, timedelta


class MockSource:
    def __init__(self, id, url, last_modified, etag, next_check_time):
        self.id = id
        self.url = url
        self.last_modified = datetime.strptime(
            last_modified, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        self.etag = etag
        self.next_check_time = datetime.strptime(
            next_check_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) if next_check_time else None
