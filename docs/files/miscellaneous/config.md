# [`_config.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/_config.py)

This file is not a `.cfg` file placed outside of the app folder for a little easier understanding and implementation.

# URL Root / Prefix

`app.config["URL_ROOT"]` allows you to put all routes under a sub-path if needed (say it's a sub-app of another app) with the help of `Blueprints`.


## Messages

`app.config["MSG"]` allows you to replace some messages wherever possible.
`f-strings` are not supported currently.


## Features

`app.config["FEATURES"]` allows you to toggle some features using boolean values.
`True` means on, `False` means off.