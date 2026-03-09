#!/usr/bin/env python3
import contextlib
from navigator import Application
from app import Main

# define a new Application
app = Application(Main, enable_jinja2=True)

# Enable WebSockets Support
app.add_websockets()

if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt):
        app.run()