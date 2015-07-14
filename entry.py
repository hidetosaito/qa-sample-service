#!/bin/env python
# coding: utf-8

import os
from dcsqa.app import create_app

app = create_app(config='config.DevelopmentConfig')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)