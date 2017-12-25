#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'WangCY'

'''
async web application.
'''


import logging;logging.basicConfig(level=logging.INFO)
import orm
from models import User,Blog,Comment
import asyncio,os,json,time

from aiohttp import web

def index(request):
	return web.Response(body='<h1>WangCY</h1>')

async def init(loop):
	await orm.create_pool(loop=loop, user='root', password='root', db='test')
	# user = User(name='wangchunyun', email='624332772@qq.com', passwd='123456', admin=True, image='/2017/12/15/4546rr.jpg')
	# user = User(name='yunyun', email='14334332772@qq.com', created_at=1514189784.19922, passwd='7888888', admin=True, image='/2017/11/15/4ghghfhrr.jpg',id='0015141897841980b0a0929420c47a89ab4283f71aac817000')
	user = User(id='0015141897841980b0a0929420c47a89ab4283f71aac817000')
	# user = User()
	# print(await user.find('0015141897841980b0a0929420c47a89ab4283f71aac817000'))
	# print(await user.update())
	print(await user.remove())

	# app = web.Application(loop=loop)
	# app.router.add_route('GET','/',index)
	# srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
	# logging.info('server started at http://127.0.0.1:9000')
	# return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
# loop.close()


