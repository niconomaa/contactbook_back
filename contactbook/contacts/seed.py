import datetime
import random
from contacts.models import Person

for person in Person.nodes.all():
    person.delete()

for i in range(30):
    person = Person(
        mobile_phone='0800666666',
        verified=True,
        infected=False,
        incubation_start_date=None
    ).save()

for person in Person.nodes.all():
    for contacted_person in Person.nodes.all():
        if person.uid == contacted_person.uid:
            continue
        rand = random.randint(0, 10)
        if rand > 0:
            continue
        rel = person.contacted_persons.connect(contacted_person)
        rel.date = datetime.datetime.now()
        rel.location = "Unknown"
        rel.save()
