#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'WangCY'

'''
async web application.
'''

import logging;logging.basicConfig(level=logging.INFO)
import orm,asyncio,os,json,time,webcore
from models import User,Blog,Comment
from jinja2 import  Environment,FileSystemLoader
from datetime import datetime
from aiohttp import web


# def index(request):
# 	return web.Response(body='<h1>WangCY</h1>')

def init_jinjia2(app,**kw):
	logging.info('init jinja2...')
	options = dict(
		autoescape = kw.get('autoescape',True),
		block_start_string = kw.get('block_start_string','{%'),
		block_end_string = kw.get('block_end_string','%}'),
		variable_start_string = kw.get('variable_start_string','{{'),
		variable_end_string = kw.get('variable_end_string','}}'),
		auto_reload = kw.get('auto_reload',True)
	)
	path = kw.get('path',None)
	if path is None:
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
	logging.info('set jinja2 template path: %s'% path)
	env = Environment(loader=FileSystemLoader(path),**options)
	filters = kw.get('filters',None)
	if filters is not None:
		for name,f in filters.items():
			env.filters[name] = f
	app['__templating__'] = env

async def logger_factory(app,handler):
	async def logger(request):
		logging.info('Request: %s %s' % (request.method,request.path))
		# await asyncio.sleep(0.3)
		return (await handler(request))
	return logger

async def data_factory(app,handler):
	async def parse_data(request):
		if request.method == 'POST':
			if request.content_type.startswith('application/json'):
				request.__data__ = await request.json()
				logging.info('request json: %s' % str(request.__data__))
			elif request.content_type.startswith('application/x-www-form-urlencoded'):
				request.__data__ = await request.post()
				logging.info('request form: %s' % str(request.__data__))
		return (await handler(request))
	return parse_data

async def response_factory(app,handler):
	async def response(request):
		logging.info('Response handler...')
		r = await handler(request)
		if isinstance(r,web.StreamResponse):
			return r
		if isinstance(r,bytes):
			resp = web.Response(body=r)
			resp.content_type = 'application/octet-stream'
			return resp
		if isinstance(r,str):
			if r.startswith('redirect:'):
				return web.HTTPFound(r[9:])
			resp = web.Response(body=r.encode('utf-8'))
			resp.content_type = 'text/html;charset=utf-8'
			return resp
		if isinstance(r,dict):
			template = r.get('__template__')
			if template is None:
				resp = web.Response(body=json.dumps(r,ensure_ascii=False,default=lambda o:o.__dict__).encode('utf-8'))
				resp.content_type = 'application/json;charset=utf-8'
				return resp
			else:
				resp =web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
				resp.content_type = 'text/html;charset=utf-8'
				return resp
		if isinstance(r,int) and r>=100 and r<600:
			return web.Response(r)
		if isinstance(r,tuple) and len(r) == 2:
			t,m = r
			if isinstance(t,int) and t>=100 and t<600:
				return web.Response(t,str(m))
		resp = web.Response(boyd=str(r).encode('utf-8'))
		resp.content_type = 'text/plain;charset=utf-8'
		return resp
	return response

def datetime_filter(t):
	logging.info('datetime_filter...')
	delta = int(time.time()-t)
	if delta < 60:
		return '1分钟前'
	if delta < 3600:
		return '%s分钟前'% (delta//60)
	if delta < 86400:
		return '%s小时前'% (delta//3600)
	if delta < 604800:
		return '%s天前'% (delta//86400)
	dt = datetime.fromtimestamp(t)
	return '%s年%s月%s日'% (dt.year,dt.month,dt.day)


async def init(loop):
	#测试数据库功能
	# await orm.create_pool(loop=loop, user='root', password='root', db='test')
	# user = User(name='wangchunyun', email='624332772@qq.com', passwd='123456', admin=True, image='/2017/12/15/4546rr.jpg')
	# await user.save()
	# user = User(name='yunyun', email='14334332772@qq.com', created_at=1514189784.19922, passwd='7888888', admin=True, image='/2017/11/15/4ghghfhrr.jpg',id='0015141897841980b0a0929420c47a89ab4283f71aac817000')
	# user = User(id='0015141897841980b0a0929420c47a89ab4283f71aac817000')
	# user = User()
	# print(await user.find('0015141897841980b0a0929420c47a89ab4283f71aac817000'))
	# print(await user.update())
	# print(await user.remove())

	#测试web核心代码
	await orm.create_pool(loop=loop, user='root', password='root', db='test')
	app = web.Application(loop=loop,middlewares=[
		logger_factory, response_factory
	])
	init_jinjia2(app,filters=dict(datetime=datetime_filter))
	webcore.add_routes(app,'handlers')
	webcore.add_static(app)
	srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
	logging.info('server started at http://127.0.0.1:9000')
	return srv

	# app = web.Application(loop=loop)
	# app.router.add_route('GET','/',index)
	# srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
	# logging.info('server started at http://127.0.0.1:9000')
	# return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()



