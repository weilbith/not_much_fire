import gi
gi.require_version("Notify", "0.7")

from gi.repository import GLib
from os import path, makedirs
from datetime import datetime, date, timedelta


class Cache:
    date_format = "%a, %d %b %Y %H:%M:%S"

    def __init__(self, app_name):
        self.cache_file = path.join(
            GLib.get_user_cache_dir(), app_name, "last_update"
        )

        cache_folder = path.dirname(self.cache_file)

        if not path.exists(cache_folder):
            makedirs(cache_folder)

    @property
    def last_update(self):
        """Parses the timestamp when messages have been notified the last time.

        In case the last cached timestamp is not from today, return the minimal
        date to notifiy all messages again for the first time today.
        """

        timestamp = None

        try:
            date_string = open(self.cache_file, "r").read()
            timestamp = datetime.strptime(date_string, self.date_format)

        except Exception:
            timestamp = datetime.min

        yesterday = date.today() - timedelta(days=1)

        if timestamp.date() <= yesterday:
            timestamp = datetime.min

        return timestamp

    def update(self):
        """Stores the current timestamp formatted into the cache file.

        This is intended to be called after all messages have been handled for
        the current state.
        """

        with open(self.cache_file, "w") as cache:
            cache.write(datetime.now().strftime(self.date_format))
