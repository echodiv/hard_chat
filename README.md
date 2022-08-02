# Social WEB service
This service provides the ability to send messages not only to your friends, but to all users of the social network.
For those users who write the most interesting (in your opinion) notes, you can subscribe and follow each entry. And don't lose a single precious symbol.
You can watch the stream of all entries and, of course, find a lot of useful information there.
You can send private messages because there are some thoughts that are better said in person. Are there the same?
You can use the post search to find what you might be missing.

# Technology
Create using Flask, sqlAlchemy and other

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
