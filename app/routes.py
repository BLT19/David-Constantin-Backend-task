from app import app
import pandas as pd
import json
from datetime import datetime
import re

table = pd.read_excel('Tick Sightings.xlsx', dtype={'id':str, 'date':str, 'location':str, 'species':str, 'latinName':str})

@app.errorhandler(404)
def bad_request(error):
    return error, 404

@app.route('/')
def index():
    return table.to_json(orient='records')

@app.route('/city', defaults={'item': None})
@app.route('/city/<item>')
def city(item):
    def use_regex(input_item):
        pattern = re.compile(r"[A-Z][a-z]+")
        return pattern.match(input_item)
    
    if item:
        if use_regex(item):
            sightings = table[table['location'] == item]

            total_entries = sightings.shape[0]
            result = {'total_entries': total_entries, 'data': sightings.to_json(orient='records')}
    
            return json.dumps(result)
        else:
            return bad_request('Invalid input (The first letter of the city must be capitalised)')
    else:
        return table.to_json(orient='records')

@app.route('/date', defaults={'after': None, 'before': None})
@app.route('/date/after=<after>', defaults={'before': None})
@app.route('/date/before=<before>', defaults={'after': None})
@app.route('/date/after=<after>before=<before>')
def date(after, before):
    table['date'] = pd.to_datetime(table['date'])
    if after and before:
        after = pd.to_datetime(after)
        before = pd.to_datetime(before)

        temp = table[table['date'] > after]
        sightings = temp[temp['date'] < before]
        return sightings.to_json(orient='records', date_format='iso')
    elif after:
        after = pd.to_datetime(after)

        sightings = table[table['date'] > after]
        return sightings.to_json(orient='records', date_format='iso')
    elif before:
        before = pd.to_datetime(before)

        sightings = table[table['date'] < before]
        return sightings.to_json(orient='records', date_format='iso')
    else:
        table['date'] = table['date'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        return table.to_json(orient='records')