# -*- coding: utf-8 -*-

"""Polls web app views."""

import json

from aiohttp import web

from bson import ObjectId
from bson.json_util import dumps as bson_dumps

from cerberus import Validator


JSON_TYPE = 'application/json'
HTTP_BAD_REQUEST = web.HTTPBadRequest.status_code
HTTP_CREATED = web.HTTPCreated.status_code
HTTP_NO_CONTENT = web.HTTPNoContent.status_code
HTTP_OK = web.HTTPOk.status_code


def validate_schema(document, schema):
    validator = Validator(schema)
    if not validator.validate(document):
        raise web.HTTPBadRequest(
                body=json.dumps(validator.errors),
                content_type=JSON_TYPE)
    return validator.document


class ItemListView(web.View):

    collection = 'items'

    list_query = {
        'page': {
            'type': 'integer',
            'coerce': int,
            'min': 1,
        },
        'limit': {
            'type': 'integer',
            'coerce': int,
            'min': 1,
        },
    }
    create_query = {
    }

    async def get(self):
        """List items view."""
        schema = self.list_query
        query = validate_schema(dict(self.request.query), schema)
        page = query.get('page', 1)
        limit = query.get('limit', 20)
        skip = (page - 1) * limit
        db = self.request.app['db']
        items = [item async for item in
                 db[self.collection].find().skip(skip).limit(limit)]
        return web.json_response(items, status=HTTP_OK, dumps=bson_dumps)

    async def post(self):
        """Create item view."""
        # schema = self.create_query
        # query = validate_schema(dict(self.request.query), schema)
        db = self.request.app['db']
        data = await self.request.json()
        if not data:
            raise web.HTTPBadRequest(
                    reason='no POST data',
                    content_type=JSON_TYPE)
        item = await db[self.collection].insert_one(data)
        item_id = item.inserted_id
        item_url = self.request.app.router['item-detail'].url_for(id=str(item_id))
        return web.json_response(
                item_id,
                status=HTTP_CREATED,
                headers={'Location': str(item_url)},
                dumps=bson_dumps)


class ItemDetailView(web.View):

    collection = 'items'

    retrieve_query = {
    }
    update_query = {
    }
    delete_query = {
    }

    async def get(self):
        """Retrieve item view."""
        # schema = self.retrieve_query
        # query = validate_schema(dict(self.request.query), schema)
        item_id = self.request.match_info['id']
        db = self.request.app['db']
        item = await db[self.collection].find_one(ObjectId(item_id))
        if not item:
            raise web.HTTPNotFound(reason='item not found', content_type=JSON_TYPE)
        return web.json_response(item, status=HTTP_OK, dumps=bson_dumps)

    async def put(self):
        """Update item view."""
        # schema = self.update_query
        # query = validate_schema(dict(self.request.query), schema)
        item_id = self.request.match_info['id']
        data = await self.request.json()
        db = self.request.app['db']
        result = await db[self.collection].replace_one(
                {'_id': ObjectId(item_id)},
                data)
        if not result.modified_count > 0:
            raise web.HTTPNotFound(reason='item not found', content_type=JSON_TYPE)
        return web.json_response({}, status=HTTP_OK, dumps=bson_dumps)

    async def patch(self):
        """Partial update item view."""
        # schema = self.update_query
        # query = validate_schema(dict(self.request.query), schema)
        item_id = self.request.match_info['id']
        data = await self.request.json()
        db = self.request.app['db']
        result = await db[self.collection].update_one(
                {'_id': ObjectId(item_id)},
                {'$set': data})
        if not result.modified_count > 0:
            raise web.HTTPNotFound(reason='item not found', content_type=JSON_TYPE)
        return web.json_response({}, status=HTTP_OK, dumps=bson_dumps)

    async def delete(self):
        """Delete item view."""
        # schema = self.delete_query
        # query = validate_schema(dict(self.request.query), schema)
        item_id = self.request.match_info['id']
        db = self.request.app['db']
        item = await db[self.collection].delete_one({'_id': ObjectId(item_id)})
        if not item.deleted_count > 0:
            raise web.HTTPNotFound(
                    reason='no item to delete',
                    content_type=JSON_TYPE)
        return web.json_response({}, status=HTTP_NO_CONTENT)
