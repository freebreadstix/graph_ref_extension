from flask import Flask, request
from neo4j import GraphDatabase
import graph_functions as gf
import json
from datetime import datetime

app = Flask(__name__)

uri = "neo4j://localhost:7687"



@app.route('/')
def hello_world():
    return "Hello world"


@app.route('/reference-db', methods=['POST'])
def add_reference():
    """
    Takes form data from POST request and adds to graph database
    Request format:

    Required fields
    alias -- unique name of reference
    time -- date and time reference is added

    Optional fields
    link -- reference url
    relationships -- nested json of related references and relationship
    """
    
    alias = request.form['alias']
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    date = now.strftime('%m/%d/%Y')

    link = request.form['link']

    rel_dict = {}
    for relationship in ['rel1', 'rel2', 'rel3']:
        node, relationship = request.form[relationship].split(':')
        if node[0] != '[': # TODO fix this boolean condition
            rel_dict[node] = relationship
    
    with driver.session() as session:
        alias_present = gf.check_reference(session, alias)
        if not alias_present:
            session.write_transaction(gf.add_reference, alias, time, date, link)

            if len(rel_dict) > 0:
                for related, relationship in rel_dict.items():
                    session.write_transaction(gf.add_relationship, alias, related, relationship)
            return "Success"
        else:
            return "Alias already exists"
    

@app.route('/test', methods=['POST'])
def test_form():
    alias = request.form['alias']

    print(type(alias))

if __name__ == "__main__":
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    app.run(debug=True, port=5000)

    driver.close()