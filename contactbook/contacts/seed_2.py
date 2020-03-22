import datetime
from contacts.models import Person

# Delete all present nodes and relationship
for person in Person.nodes.all():
    person.delete()

nico = Person(mobile_phone='0800666666', verified=True, infected=False).save()
jonas = Person(mobile_phone='0800777777', verified=True, infected=False).save()
lukas = Person(mobile_phone='0800888888', verified=True, infected=False).save()

rel = nico.contacted_persons.connect(jonas)
rel.date = datetime.datetime.now() - datetime.timedelta(days=5)
rel.save()

rel = nico.contacted_persons.connect(jonas)
rel.date = datetime.datetime.now()
rel.save()

rel = nico.contacted_persons.connect(lukas)
rel.date = datetime.datetime.now() - datetime.timedelta(days=1)
rel.location = "Unknown"
rel.save()

rel = nico.contacted_persons.connect(lukas)
rel.date = datetime.datetime.now() - datetime.timedelta(days=3)
rel.save()

rel = nico.contacted_persons.connect(lukas)
rel.date = datetime.datetime.now() - datetime.timedelta(days=4)
rel.save()