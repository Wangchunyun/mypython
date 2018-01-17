#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
request handler
'''

__author__ = 'WangCY'

from webcore import get,post
from models import User,Blog,Comment
import asyncio


@get('/')
async def index(request):
    users = await User.fetchAll()
    return {
        '__template__':'test.html',
        'users':users
    }