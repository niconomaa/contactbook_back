### Create Django app environment

virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
python3 contactbook/manage.py runserver # to run the server

### Create Docker container for Neo4j database

* Download Docker Desktop and run it.
* Run the following command to create the Docker container:
```
docker run \
    --name contactbook_dev \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    neo4j:latest
```

# graphene information
one schema.py in main folder, one query wrapping all other queries
one schema.py in every application

in main urls.py include graphql endpoint