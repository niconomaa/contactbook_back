virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
python3 contactbook/manage.py runserver # to run the server
