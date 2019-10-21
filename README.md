# Not Much Fire

A simple [Notmuch](https://notmuchmail.org) notification tool

- [Installation](#installation)
- [Usage](#usage)
- [Notmuch Hook](#notmuch-hook)

## Installation

Install it globally with [pip](https://pip.pypa.io/en/stable):

```shell
$ pip install not-much-fire
```

Execute always the most recent version with [pipx](https://pipxproject.github.io/pipx/):

```shell
$ pipx run not-much-fire
```

## Usage

```shell
$ not-much-fire --help

Usage: not-much-fire [OPTIONS]

  A simple Notmuch notification tool.

  Requests Notmuch for new unread messages and send notifications to the
  desktop environment. Already notified messages get not shown again for a
  whole day. If they remain unread, they get are handled again on the next
  day.

Options:
  --notmuch-query <query>  Used to query the unread messages from the Notmuch
                          database  [default: is:unread and is:inbox]
  --help                   Show this message and exit.
```

## Notmuch Hook

To get notification each time after `notmuch` has updated its database, add
a new hook. Therefore add a new line like the following into
`$DATABASE/.notmuch/hooks/post-new`.

```shell
#!/bin/bash
not-much-fire
# or: pipx run not-much-fire
```

Checkout `man notmuch-hooks` to get further information about hooks and
`notmuch`. I recommend to set the `$NOTMUCH_CONFIG` environment variable to
reach compatibility with the [XDG base directory
standard](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).
