virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
python3 contactbook/manage.py runserver # to run the server

# graphene information
one schema.py in main folder, one query wrapping all other queries
one schema.py in every application

in main urls.py include graphql endpoint