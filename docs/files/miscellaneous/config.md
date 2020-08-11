# [`_config.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/_config.py)

This file is not a `.cfg` file placed outside of the app folder for a little easier understanding and implementation.

# URL Root / Prefix

`app.config["URL_ROOT"]` allows you to put all routes under a sub-path if needed (say it's a sub-app of another app) with the help of `Blueprints`.


## Templates

`app.config["TEMPLATES"]` makes it easy to switch templates that are rendered through the app.


## Messages

`app.config["MSG"]` allows you to replace some messages wherever possible.
`f-strings` are not supported currently.


## Features

`app.config["FEATURES"]` allows you to toggle some features using boolean values.
`True` means on, `False` means off.

### `ONE_TIME_USE`

Allows users to use the bot without having their credentials stored in the database. This means that their calendar is fetched ONCE and remains in the app for a limited time.

### `DEMO`

Allows demonstration of the bot outside of the platform using embedded chats, etc. This uses a unique ID (usually session ID) as the sender ID. All demo users are forced one-time-use i.e. their credentials aren't stored and the chat dies after a while.