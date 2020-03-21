## Set up Django app environment

virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
python3 contactbook/manage.py runserver # to run the server

# graphene information
one schema.py in main folder, one query wrapping all other queries
one schema.py in every application

in main urls.py include graphql endpoint


## Setup database

### Create Docker container for Neo4j database

* Download Docker Desktop and run it.
* Run the following command to create the Docker container:
```
docker run \
    --name contactbook_dev \
    -p7474:7474 -p7687:7687 \
    -d \
    --env NEO4J_AUTH=neo4j/contactbook \
    neo4j:3.5
```
Version 3.5 is required in order to utilize the neomodel package as an ORM in the Django app.

### Use Django shell to query database

* `python manage.py shell`


