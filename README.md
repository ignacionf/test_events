# test_events

## First Start

Install `pipenv`:

```
$ pip install pipenv
or
$ brew install pipenv
or
$ sudo apt install pipenv
```

Then:

```
$ pipenv install
$ pipenv run python manage.py migrate
$ pipenv run python manage.py loaddata fixture/groups.json
$ pipenv run ./manage.py createsuperuser --email admin@admin.com --username admin
$ pipenv run python manage.py runserver
```

## Use

First you have to generate users, rooms and events. Then you have to generate the cookie for each user from the admin login since we are not using any token authentication system (rest framework, simple jwt, etc)
To differentiate client users from business users, they must be assigned to the corresponding group.

### Operate with rooms

List:
```
curl 'http://localhost:8000/room/' \
  -H 'Cookie: csrftoken=<get from browser cookies>; sessionid=<get from browser cookies>' \
  --compressed -X GET
```

Create:
```
curl 'http://localhost:8000/room/' \
  -H 'Cookie: csrftoken=<get from browser cookies>; sessionid=<get from browser cookies>' \
  -d '{"name":"Name of room", "capacity": 2}' \
  -H "Content-Type: application/json" -H "Accept: application/json" --compressed --silent -X POST
```

Detail:
```
curl 'http://localhost:8000/room/<pk>/' \
  -H 'Cookie: csrftoken=<get from browser cookies>; sessionid=<get from browser cookies>' \
  --compressed --silent -X GET
```

Delete:
```
curl 'http://localhost:8000/room/<pk>/' \
  -H 'Cookie: csrftoken=<get from browser cookies>; sessionid=<get from browser cookies>' \
  --compressed --silent -X DELETE
```

### Operate with events:

Same as rooms but you need replace `room` by `event`.

Create:
```
curl 'http://localhost:8000/event/' \
  -H 'Cookie: csrftoken=<get from browser cookies>; sessionid=<get from browser cookies>' \
  -H "Content-Type: application/json" \
  -d '{"name":"Event 1", "private":false, "room": <room id>, "date": "2022-09-09"}' \
  -H "Content-Type: application/json" -H "Accept: application/json" --compressed --silent -X POST
```

### Book and unbook via curl:

Book:
```
curl 'http://localhost:8000/event/2/book/' \
  -H 'Cookie: csrftoken=<get from browser cookies>; sessionid=<get from browser cookies>' \
  --compressed -X POST
```

Unbook:
```
curl 'http://localhost:8000/event/2/book/' \
  -H 'Cookie: csrftoken=<get from browser cookies>; sessionid=<get from browser cookies>' \
  --compressed -X DELETE
```
