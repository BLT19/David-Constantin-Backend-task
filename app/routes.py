from app import app
import pandas as pd
import json

table = pd.read_excel('Tick Sightings.xlsx', dtype={'id':str, 'date':str, 'location':str, 'species':str, 'latinName':str})
@app.route('/')
def index():
    return table.to_json(orient='records')

@app.route('/city/<item>')
def city(item):
    sightings = table[table['location'] == item]

    arr = sightings.to_dict(orient='records')
    
    return json.dumps(arr)
   