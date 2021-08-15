# Social WEB service
Create using Flask, sqlAlchemy
## Modules:
### 1. auth
- login
- logout
- registration
- reset password
### 2. errors
### 3. main
- get user profile
- edit user profile
- following
- get followed posts
### 4. messages
- send message
- get message
### 5. api

## Build docker with flask application
> docker build -t microblog:latest .

## Settings

1. Environment variables 

> [export | set ] FLASK_APP=run.py

2. flask run --host 0.0.0.0

## Elasticsearch

1. Install docker

> sudo apt install docker

2. Pull docker image

> docker pull docker.elastic.co/elasticsearch/elasticsearch:7.10.0

3. Run docker image

> docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.0

4. Ckeck node
> curl -X GET "localhost:9200/_cat/nodes?v&pretty" 

## Database migration:

1. Create Migration State

> flask db migrate -m "Whate new for migration"

2. Updgrade or Downgrade

> flask db [ upgrade | downgrade ]

## Multilanguage
1. Create .pot file

> pybabel extract -F babel.cfg -k _l -o messages.pot .

2.1. Create language directory from .pot file
> pybabel init -i messages.pot -d app/translations -l ru

2.2 Update langeage directory with new text
> pybabel update -i messages.pot -d app/translations

3. Compile tanguage packet
> pybabel compile -d app/translations

## For Test:
1. shell with flask

> flask shell

2. Test mail server

> python -m smtpd -n -c DebuggingServer localhost:8025
