# -*- coding: utf-8 -*-

import web
from wechat_service.handle import Handle

urls = (
    '/wx', 'Handle',
)

app = web.application(urls, globals())

if __name__ == '__main__':
    # app = web.application(urls, globals())
    app.run()
