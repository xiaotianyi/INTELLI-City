# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle

urls = (
    '/wx', 'Handle',
)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
