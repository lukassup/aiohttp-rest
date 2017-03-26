# Python + MongoDB async web app

Uses `aiohttp` async web framework, `motor` async MongoDB engine and `cerberus`
for schema validation.

## Install

```bash
$ git clone https://github.com/lukassup/aiohttp-rest
$ cd aiohttp-mongo
$ python -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ docker run -p 27017:27017 -n mongo mongo
$ python main.py
```

## Usage

This is the API URLs, supported methods and corresponding views

```
GET     /     item-list
POST    /     item-list
GET     /:id  item-detail
PUT     /:id  item-detail
PATCH   /:id  item-detail
DELETE  /:id  item-detail
```

List all items

```bash
$ http GET 'http://localhost:8080/'
```
```
HTTP/1.1 200 OK
Content-Length: 132
Content-Type: application/json; charset=utf-8
Date: Sun, 26 Mar 2017 01:54:03 GMT
Server: Python/3.6 aiohttp/2.0.3
```
```json
[
    {
        "_id": {
            "$oid": "58d71f31137a002d415560e4"
        },
        "body": "Hello!"
    },
    {
        "_id": {
            "$oid": "58d71f31137a002d415560e5"
        },
        "body": "Goodbye."
    }
]
```

Create an item

```bash
$ http POST 'http://localhost:8080/' nickname='lukassup'
```
```
HTTP/1.1 201 Created
Content-Length: 36
Content-Type: application/json; charset=utf-8
Date: Sun, 26 Mar 2017 01:54:21 GMT
Location: /58d71f62137a002d415560e6
Server: Python/3.6 aiohttp/2.0.3
```
```json
{
    "$oid": "58d71f62137a002d415560e6"
}
```

Retrieve an item

```bash
$ http GET 'http://localhost:8080/58d71f62137a002d415560e6'
```
```
HTTP/1.1 200 OK
Content-Length: 69
Content-Type: application/json; charset=utf-8
Date: Sun, 26 Mar 2017 01:54:28 GMT
Server: Python/3.6 aiohttp/2.0.3
```
```json
{
    "_id": {
        "$oid": "58d71f62137a002d415560e6"
    },
    "nickname": "lukassup"
}
```
