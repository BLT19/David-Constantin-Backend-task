from app import app
import pandas as pd
import json
from datetime import datetime
import re
import werkzeug.exceptions

table = pd.read_excel('Tick Sightings.xlsx', dtype={'id':str, 'date':str, 'location':str, 'species':str, 'latinName':str})

@app.route('/')
def index():
    return json.dumps(table.to_dict(orient='records'))

@app.route('/city', defaults={'item': None})
@app.route('/city/<item>')
def city(item):
    def use_regex(input_item):
        pattern = re.compile(r"[A-Z][a-z]+")
        return pattern.match(input_item)
    
    if use_regex(item):
        if item:
            sightings = table[table['location'] == item]

            arr = sightings.to_dict()
            total_entries = sightings.shape[0]
            result = {'total_entries': total_entries, 'data': arr}
    
            return json.dumps(result)
    
        else:
            return 0
        
    else:
        return bad_request

#@app.route('/date/<after> <before')
#def date(after, before):
#    if before is None and after is None:
#        sightings = table[table['']]