from app import app
import pandas as pd
import json
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('Tick Sightings.xlsx', dtype={'id':str, 'date':str, 'location':str, 'species':str, 'latinName':str})
df['date'] = pd.to_datetime(df['date'])

@app.errorhandler(400)
def bad_request(error):
    return error, 400

@app.route('/')
def index():
    return df.to_json(orient='records', date_format='iso')

@app.route('/city', defaults={'item': None})
@app.route('/city/<item>')
def city(item):
    def use_regex(input_item):
        pattern = re.compile(r"[A-Z][a-z]+")
        return pattern.match(input_item)
    
    if item:
        if use_regex(item):
            sightings = df[df['location'] == item]

            total_entries = sightings.shape[0]
            result = {'total_entries': total_entries, 'data': sightings.to_json(orient='records', date_format='iso')}
    
            return json.dumps(result)
        else:
            return bad_request('Invalid input (The first letter of the city must be capitalised)')
    else:
        return df.to_json(orient='records',date_format='iso')

@app.route('/date', defaults={'after': None, 'before': None})
@app.route('/date/after=<after>', defaults={'before': None})
@app.route('/date/before=<before>', defaults={'after': None})
@app.route('/date/after=<after>before=<before>')
def date(after, before):
    def use_regex(input_item):
        pattern = re.compile(r"^([0-9]+-(0[1-9]|1[0,1,2])-(0[1-9]|[12][0-9]|3[01])T(0?[0-9]|1[0-9]|2[0-3]):(0?[0-9]|[1-5][0-9]):(0?[0-9]|[1-5][0-9]){19})$")
        return pattern.match(input_item)

    if after and before:
        if use_regex(after) and use_regex(before):
            after = pd.to_datetime(after)
            before = pd.to_datetime(before)

            temp = df[df['date'] > after]
            sightings = temp[temp['date'] < before]
            return sightings.to_json(orient='records', date_format='iso')
        
        else:
            return bad_request('Invalid input (Dates must be in the format YYYY-mm-ddThh:mm:ss)')
    elif after:
        if use_regex(after):
            after = pd.to_datetime(after)

            sightings = df[df['date'] > after]
            return sightings.to_json(orient='records', date_format='iso')
        
        else:
            return bad_request('Invalid input (Dates must be in the format YYYY-mm-ddThh:mm:ss)')
    elif before:
        if use_regex(before):
            before = pd.to_datetime(before)

            sightings = df[df['date'] < before]
            return sightings.to_json(orient='records', date_format='iso')
        
        else:
            return bad_request('Invalid input (Dates must be in the format YYYY-mm-ddThh:mm:ss)')
    else:
        return df.to_json(orient='records', date_format='iso')
    
@app.route('/trend/weekly/year=<year>month=<month>')
def weekly(year, month):
    def use_regex(input_item):
        pattern = re.compile(r"^[0-9]{4}$")
        return pattern.match(input_item)