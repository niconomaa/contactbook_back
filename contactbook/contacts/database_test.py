from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://0.0.0.0:7687", auth=("neo4j", "contactbook"))

def add_contact(tx, name, contact_name):
    tx.run("MERGE (a:Contact {name: $name}) "
           "MERGE (a)-[:HAS_TOUCHED]->(b:Contact {name: $contact_name})",
           name=name, contact_name=contact_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Contact)-[:HAS_TOUCHED]->(b) WHERE a.name = $name "
                         "RETURN b.name ORDER BY b.name", name=name):
        print(record["b.name"])

with driver.session() as session:
    session.write_transaction(add_contact, "Arthur", "Guinevere")
    session.write_transaction(add_contact, "Arthur", "Lancelot")
    session.write_transaction(add_contact, "Arthur", "Merlin")
    session.read_transaction(print_friends, "Arthur")

driver.close()
