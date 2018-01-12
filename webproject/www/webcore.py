#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'WangCY'


import aiohttp,os,inspect,logging,functools
from urllib import parse
from aiohttp import web
from APIerror import APIError


def get(path):
    '''
    definded decorator @get('/path')
    :param path:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__methord__ = 'get'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
    definded decorator @post('/path')
    :param path:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__methord__ = 'post'
        wrapper.__route__ = path
        return wrapper
    return decorator

