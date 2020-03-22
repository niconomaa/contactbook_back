import datetime
import random
from contacts.models import Person

# Delete all present nodes and relationship
for person in Person.nodes.all():
    person.delete()

for i in range(30):
    person = Person(
        mobile_phone=random.randint(10000000, 99999999),    # Random mobile phone number with 8 digits
        verified=True,
        infected=False,
        incubation_start_date=None,
        danger="0"
    ).save()

for person in Person.nodes.all():
    for contacted_person in Person.nodes.all():
        if person.uid == contacted_person.uid:
            continue
        rand = random.randint(0, 10)
        if rand > 0:
            continue
        rel = person.contacted_persons.connect(contacted_person)
        # TODO: Generate random datetime within last days.
        rel.date = datetime.datetime.now()
        rel.location = "Unknown"
        rel.save()