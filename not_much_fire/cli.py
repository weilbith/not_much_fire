from datetime import timedelta

import click

from not_much_fire.cache import Cache
from not_much_fire.database import Database
from not_much_fire.notifier import Notifier

_APP_NAME = "not-much-fire"


def validate_time_delta(ctx, param, value: str) -> timedelta:
    time_delta_parts = value.split(":")

    if (
        len(time_delta_parts) != 3
        and all(len(part) == 2 for part in time_delta_parts)
        and all(part.isdigit() for part in time_delta_parts)
    ):
        raise click.BadParameter(
            "The time-delta format must be 'hh:mm:ss' ({value})!"
        )

    return timedelta(
        hours=int(time_delta_parts[0]),
        minutes=int(time_delta_parts[1]),
        seconds=int(time_delta_parts[2]),
    )


@click.command()
@click.option(
    "--notmuch-query",
    help="Used to query the unread messages from the Notmuch database",
    type=str,
    default="is:unread and is:inbox",
    show_default=True,
)
@click.option(
    "--time-delta",
    help=(
        "Amount of time, which when passed since the last notification of a mail, "
        "it gets notified again if still unread. It must follow the format: 'hh:mm:ss'."
    ),
    type=str,
    default="24:00:00",
    show_default=True,
    callback=validate_time_delta,
)
def main(notmuch_query: str, time_delta: timedelta):
    """A simple Notmuch notification tool.

    Requests Notmuch for new unread messages and send notifications to
    the desktop environment. Already notified messages get shown again
    after a specific amount of time if they remain unread.
    """

    cache = Cache(_APP_NAME, time_delta)
    database = Database(cache, notmuch_query)
    notifier = Notifier(_APP_NAME)

    for message in database.filtered_messages:
        notifier.notify_message(message)

    cache.update()
