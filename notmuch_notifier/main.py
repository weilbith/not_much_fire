from cache import Cache
from database import Database
from notifier import Notifier


APP_NAME = "notmuch-notifier"


cache = Cache(APP_NAME)
database = Database(cache)
notifier = Notifier(APP_NAME)

for message in database.filtered_messages:
    notifier.notify_message(message)

cache.update()
