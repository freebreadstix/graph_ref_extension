from neo4j import GraphDatabase


def add_reference(tx, alias, time, date, link=None):
    if link:
        query = "CREATE (r:reference {alias: $alias, time: $time, date: $date, link: $link})"
        tx.run(query, alias=alias, time=time, date=date, link=link)
    else:
        query = "CREATE (r:reference {alias: $alias, time: $time, date: $date})"
        tx.run(query, alias=alias, time=time, date=date)

def check_reference(tx, alias):
    """
    Returns boolean for reference presence in database
    """
    query = "MATCH (n) \
        WHERE n.alias=$alias \
        RETURN n"
    results = tx.run(query, alias=alias)

    return True if results.single() else False

def add_relationship(tx, curr, related, relationship):
    query = "MATCH (a:reference), (b:reference) \
            WHERE a.alias=$curr AND b.alias=$related \
            CREATE (a)-[x:RELTYPE {relationship: $relationship}]->(b)"
    
    tx.run(query, curr=curr, related=related, relationship=relationship)

def delete_reference(tx, alias):
    query = "MATCH (n) \
            WHERE n.alias=$alias \
            DELETE (n)"
    tx.run(query, alias=alias)





