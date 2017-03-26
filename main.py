from pathlib import Path
from urllib.parse import quote_plus

import asyncio
import motor.motor_asyncio
import uvloop
import yaml

from aiohttp import web

from rest.routes import setup_routes


def yaml_load(path):
    with open(path) as yaml_file:
        return yaml.load(yaml_file)


async def init_db(app):
    conf = app['config'].get('db')
    uri = 'mongodb://{host}:{port}/{database}'
    db_settings = {
        'host': conf.get('host', 'localhost'),
        'port': conf.get('port', 27017),
        'database': conf.get('database', 'app')
    }
    username = conf.get('username')
    password = conf.get('password')
    if username:
        db_settings['username'] = quote_plus(username)
        uri = 'mongodb://{username}@{host}:{port}/{database}'
    if username and password:
        db_settings['password'] = quote_plus(password)
        uri = 'mongodb://{username}:{password}@{host}:{port}/{database}'
    client = motor.motor_asyncio.AsyncIOMotorClient(
                uri.format(**db_settings))
    db = client.get_default_database()
    app['db'] = db
    await db.items.drop()
    await db.items.insert_one({'body': 'Hello!'})
    await db.items.insert_one({'body': 'Goodbye.'})


async def close_db(app):
    pass


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

conf = yaml_load(Path('.') / 'rest' / 'conf' / 'app.yaml')
loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
app['config'] = conf
setup_routes(app)
app.on_startup.append(init_db)
app.on_cleanup.append(close_db)
listen_host = conf['app'].get('host', 'localhost')
listen_port = conf['app'].get('post', 8080)
web.run_app(app, host=listen_host, port=listen_port)
